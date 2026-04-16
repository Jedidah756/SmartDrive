from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import ListView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User
from apps.schedules.services import ensure_daily_trips

from .forms import TripUpdateForm
from .models import TripUpdate, Trip


class DriverTripUpdateView(RoleRequiredMixin, View):
    allowed_roles = (User.Role.DRIVER,)

    def post(self, request, trip_id):
        trip = get_object_or_404(Trip, pk=trip_id, driver=request.user)
        form = TripUpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.trip = trip
            update.save()
            trip.status = update.status
            if update.status == Trip.Status.DEPARTED and not trip.actual_departure:
                trip.actual_departure = timezone.now()
            if update.status == Trip.Status.ARRIVED:
                trip.actual_arrival = timezone.now()
            trip.save(update_fields=["status", "actual_departure", "actual_arrival"])
            messages.success(request, "Trip update submitted.")
        else:
            messages.error(request, "Please correct the trip update fields.")
        return redirect("accounts:driver-dashboard")


class TripHistoryView(RoleRequiredMixin, ListView):
    template_name = "driver/trip_history.html"
    context_object_name = "trips"
    allowed_roles = (User.Role.DRIVER,)

    def get_queryset(self):
        return Trip.objects.filter(driver=self.request.user).select_related("schedule__route", "schedule__vehicle")


class LiveTripPositionsView(LoginRequiredMixin, View):
    def get(self, request):
        ensure_daily_trips()
        updates = (
            TripUpdate.objects.select_related("trip__schedule__route", "trip__schedule__vehicle")
            .exclude(latitude__isnull=True)
            .exclude(longitude__isnull=True)
            .order_by("trip_id", "-timestamp")
        )
        latest_by_trip = {}
        for update in updates:
            # Polling clients only need the newest coordinate per trip, so we collapse the feed server-side.
            if update.trip_id not in latest_by_trip:
                latest_by_trip[update.trip_id] = {
                    "trip_id": update.trip_id,
                    "route": update.trip.schedule.route.name,
                    "vehicle": update.trip.schedule.vehicle.plate_number,
                    "status": update.status,
                    "latitude": float(update.latitude),
                    "longitude": float(update.longitude),
                    "note": update.note,
                    "timestamp": update.timestamp.isoformat(),
                    "stops": update.trip.schedule.route.stops_json,
                }
        return JsonResponse({"results": list(latest_by_trip.values())})


class TripUpdatesView(LoginRequiredMixin, View):
    def get(self, request, trip_id):
        trip = get_object_or_404(Trip.objects.select_related("schedule__route"), pk=trip_id)
        updates = list(trip.updates.values("status", "note", "timestamp", "latitude", "longitude")[:20])
        return JsonResponse({"trip_id": trip.id, "route": trip.schedule.route.name, "updates": updates})


class TripSummaryStatsView(LoginRequiredMixin, View):
    def get(self, request):
        today = ensure_daily_trips()
        stats = Trip.objects.filter(trip_date=today).values("status").annotate(total=Count("id"))
        return JsonResponse({"date": today.isoformat(), "results": list(stats)})
