from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User
from apps.schedules.services import ensure_daily_trips
from apps.trips.models import Trip

from .forms import BookingForm
from .models import Booking


class BookingListView(RoleRequiredMixin, ListView):
    template_name = "student/bookings.html"
    context_object_name = "bookings"
    allowed_roles = (User.Role.STUDENT,)

    def get_queryset(self):
        return Booking.objects.filter(student=self.request.user).select_related("trip__schedule__route", "trip__schedule__vehicle")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ensure_daily_trips()
        context["available_trips"] = Trip.objects.filter(status__in=[Trip.Status.SCHEDULED, Trip.Status.DEPARTED, Trip.Status.EN_ROUTE])
        return context


class BookingCreateView(RoleRequiredMixin, CreateView):
    template_name = "student/booking_form.html"
    form_class = BookingForm
    success_url = reverse_lazy("bookings:list")
    allowed_roles = (User.Role.STUDENT,)

    def form_valid(self, form):
        form.instance.student = self.request.user
        messages.success(self.request, "Seat reservation submitted.")
        return super().form_valid(form)
