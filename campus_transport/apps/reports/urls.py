from django.urls import path

from .views import ReportsApiView, ReportsDashboardView

urlpatterns = [
    path("", ReportsDashboardView.as_view(), name="dashboard"),
    path("api/summary/", ReportsApiView.as_view(), name="api-summary"),
]
