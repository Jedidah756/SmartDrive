from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import FormView, ListView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User
from apps.schedules.models import Schedule
from apps.trips.models import Trip, TripUpdate

from .forms import DriverLoginForm


class DriverLoginView(FormView):
    template_name = "driver/login.html"
    form_class = DriverLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_driver:
                return redirect("accounts:driver-dashboard")
            return redirect("accounts:dashboard-redirect")
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, "Welcome back, driver. Your shift summary is ready.")
        return redirect("accounts:driver-dashboard")


class DriverRoutesView(RoleRequiredMixin, ListView):
    template_name = "driver/routes.html"
    context_object_name = "schedules"
    allowed_roles = (User.Role.DRIVER,)

    def get_queryset(self):
        return (
            Schedule.objects.filter(driver=self.request.user)
            .select_related("route", "vehicle")
            .order_by("departure_time")
        )


class DriverTripUpdateView(RoleRequiredMixin, View):
    template_name = "driver/trip_update.html"
    allowed_roles = (User.Role.DRIVER,)

    def get_latest_trip(self, request):
        return (
            Trip.objects.filter(driver=request.user)
            .select_related("schedule__route", "schedule__vehicle")
            .order_by("-trip_date", "-scheduled_departure")
            .first()
        )

    def get(self, request):
        trip = self.get_latest_trip(request)
        return render(request, self.template_name, {"trip": trip, "status_choices": Trip.Status.choices})

    def post(self, request):
        trip = self.get_latest_trip(request)
        if not trip:
            messages.error(request, "No assigned trip found.")
            return redirect("accounts:driver-dashboard")

        status = request.POST.get("status")
        note = request.POST.get("note", "")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        valid_statuses = {s for s, _ in Trip.Status.choices}
        if status not in valid_statuses:
            messages.error(request, "Invalid trip status.")
            return redirect("driver:routes")

        TripUpdate.objects.create(
            trip=trip,
            status=status,
            note=note,
            latitude=latitude or None,
            longitude=longitude or None,
        )
        trip.status = status
        now = timezone.now()
        if status == Trip.Status.DEPARTED and not trip.actual_departure:
            trip.actual_departure = now
        if status == Trip.Status.ARRIVED:
            trip.actual_arrival = now
        trip.save(update_fields=["status", "actual_departure", "actual_arrival"])
        messages.success(request, f"Trip status updated to {trip.get_status_display()}.")
        return redirect("accounts:driver-dashboard")

