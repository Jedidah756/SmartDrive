from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView, CreateView

import logging
logger = logging.getLogger(__name__)

from apps.feedback.models import Feedback
from apps.incidents.models import Incident
from apps.schedules.services import ensure_daily_trips
from apps.trips.models import Trip
from apps.vehicles.models import Vehicle

from .forms import LoginForm, StudentRegistrationForm, DriverRegistrationForm
from .mixins import RoleRequiredMixin
from .models import User


class HomeRedirectView(RedirectView):
    pattern_name = "accounts:login"


class LoginView(FormView):
    template_name = "auth/login.html"
    form_class = LoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.success(self.request, "Welcome back. Your dashboard is ready.")
        return redirect("accounts:dashboard-redirect")


class LogoutView(LoginRequiredMixin, RedirectView):
    pattern_name = "accounts:login"

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have been signed out.")
        return HttpResponseRedirect(self.get_redirect_url(*args, **kwargs))


class StudentRegisterView(CreateView):
    template_name = "auth/register.html"
    form_class = StudentRegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(self.request, "Registration complete. You can now sign in.")
        return super().form_valid(form)


class DriverRegisterView(CreateView):
    template_name = "auth/driver_register.html"
    form_class = DriverRegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        messages.success(self.request, "Driver registration complete. You can now sign in.")
        return super().form_valid(form)


class DashboardRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        try:
            ensure_daily_trips()
        except Exception as e:
            logger.error(f"Failed to ensure daily trips: {e}")
        if self.request.user.is_student:
            return reverse_lazy("accounts:student-dashboard")
        if self.request.user.is_driver:
            return reverse_lazy("accounts:driver-dashboard")
        return reverse_lazy("accounts:admin-dashboard")


class StudentDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "student/dashboard.html"
    allowed_roles = (User.Role.STUDENT,)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user
        today = ensure_daily_trips()
        upcoming_trips = (
            Trip.objects.filter(bookings__student=student)
            .select_related("schedule__route", "schedule__vehicle")
            .order_by("scheduled_departure")[:5]
        )
        context.update(
            {
                "active_buses": Trip.objects.filter(status__in=[Trip.Status.DEPARTED, Trip.Status.EN_ROUTE]).count(),
                "trips_today": Trip.objects.filter(trip_date=today).count(),
                "student_bookings": student.bookings.count(),
                "incidents_this_week": Incident.objects.filter(reported_at__week=today.isocalendar().week).count(),
                "upcoming_trips": upcoming_trips,
                "route_feedback": Feedback.objects.filter(student=student).select_related("trip__schedule__route")[:5],
            }
        )
        return context


class DriverDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "driver/dashboard.html"
    allowed_roles = (User.Role.DRIVER,)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = ensure_daily_trips()
        trip = (
            Trip.objects.filter(driver=self.request.user, trip_date=today)
            .select_related("schedule__route", "schedule__vehicle")
            .prefetch_related("updates")
            .first()
        )
        context.update(
            {
                "trip": trip,
                "trip_status_choices": Trip.Status.choices,
                "history_count": Trip.objects.filter(driver=self.request.user).count(),
                "incident_count": Incident.objects.filter(driver=self.request.user).count(),
            }
        )
        return context


class AdminDashboardView(RoleRequiredMixin, TemplateView):
    template_name = "admin/dashboard.html"
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = ensure_daily_trips()
        active_trips = Trip.objects.filter(trip_date=today)
        context.update(
            {
                "active_buses": active_trips.filter(status__in=[Trip.Status.DEPARTED, Trip.Status.EN_ROUTE]).count(),
                "trips_today": active_trips.count(),
                "student_count": User.objects.filter(role=User.Role.STUDENT).count(),
                "incidents_this_week": Incident.objects.filter(reported_at__week=today.isocalendar().week).count(),
                "feedback_items": Feedback.objects.select_related("student", "trip__schedule__route").order_by("-created_at")[:6],
                "route_ratings": Feedback.objects.values("trip__schedule__route__name").annotate(avg_rating=Avg("rating"), total=Count("id")).order_by("-avg_rating")[:5],
                "vehicles": Vehicle.objects.order_by("plate_number")[:5],
            }
        )
        return context
