from django.urls import path

from .views import DriverLoginView, DriverRoutesView, DriverTripUpdateView

app_name = "driver"

urlpatterns = [
    path("login/", DriverLoginView.as_view(), name="login"),
    path("routes/", DriverRoutesView.as_view(), name="routes"),
    path("trip/update/", DriverTripUpdateView.as_view(), name="trip-update"),
]

