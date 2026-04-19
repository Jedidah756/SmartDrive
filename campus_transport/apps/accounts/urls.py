from django.urls import path

from .views import (
    AdminDashboardView,
    DashboardRedirectView,
    DriverDashboardView,
    DriverRegisterView,
    HomeRedirectView,
    LoginView,
    LogoutView,
    StudentDashboardView,
    StudentRegisterView,
)

urlpatterns = [
    path("", HomeRedirectView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", StudentRegisterView.as_view(), name="register"),
    path("register/driver/", DriverRegisterView.as_view(), name="driver-register"),
    path("dashboard/", DashboardRedirectView.as_view(), name="dashboard-redirect"),
    path("student/", StudentDashboardView.as_view(), name="student-dashboard"),
    path("driver/", DriverDashboardView.as_view(), name="driver-dashboard"),
    path("admin/", AdminDashboardView.as_view(), name="admin-dashboard"),
]
