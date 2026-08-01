from django.urls import path

from .views import RouteCreateView, RouteListView, RouteUpdateView

urlpatterns = [
    path("", RouteListView.as_view(), name="list"),
    path("create/", RouteCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", RouteUpdateView.as_view(), name="edit"),
]
