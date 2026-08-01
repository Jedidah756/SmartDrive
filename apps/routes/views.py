from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User

from .forms import RouteForm
from .models import Route


class RouteListView(RoleRequiredMixin, ListView):
    template_name = "admin/routes.html"
    context_object_name = "routes"
    model = Route
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)


class RouteCreateView(RoleRequiredMixin, CreateView):
    template_name = "admin/form.html"
    form_class = RouteForm
    model = Route
    success_url = reverse_lazy("routes:list")
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def form_valid(self, form):
        messages.success(self.request, "Route saved successfully.")
        return super().form_valid(form)


class RouteUpdateView(RouteCreateView, UpdateView):
    pass
