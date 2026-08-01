from django.urls import path

from .views import ScheduleCreateView, ScheduleListView, ScheduleUpdateView

urlpatterns = [
    path("", ScheduleListView.as_view(), name="list"),
    path("create/", ScheduleCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", ScheduleUpdateView.as_view(), name="edit"),
]
