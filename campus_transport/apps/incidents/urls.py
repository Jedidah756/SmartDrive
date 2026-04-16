from django.urls import path

from .views import IncidentCreateView, IncidentListView

urlpatterns = [
    path("", IncidentListView.as_view(), name="list"),
    path("create/", IncidentCreateView.as_view(), name="create"),
]
