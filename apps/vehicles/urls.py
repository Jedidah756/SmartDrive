from django.urls import path

from .views import VehicleCreateView, VehicleListView, VehicleUpdateView

urlpatterns = [
    path("", VehicleListView.as_view(), name="list"),
    path("create/", VehicleCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", VehicleUpdateView.as_view(), name="edit"),
]
