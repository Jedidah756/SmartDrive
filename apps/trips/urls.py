from django.urls import path

from .views import DriverTripUpdateView, LiveTripPositionsView, TripHistoryView, TripSummaryStatsView, TripUpdatesView

urlpatterns = [
    path("history/", TripHistoryView.as_view(), name="history"),
    path("<int:trip_id>/update/", DriverTripUpdateView.as_view(), name="update"),
    path("api/live/", LiveTripPositionsView.as_view(), name="api-live"),
    path("api/stats/", TripSummaryStatsView.as_view(), name="api-stats"),
    path("api/<int:trip_id>/updates/", TripUpdatesView.as_view(), name="api-updates"),
]
