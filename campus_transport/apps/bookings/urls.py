from django.urls import path

from .views import BookingCreateView, BookingListView

urlpatterns = [
    path("", BookingListView.as_view(), name="list"),
    path("create/", BookingCreateView.as_view(), name="create"),
]
