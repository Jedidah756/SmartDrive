from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User

from .forms import VehicleForm
from .models import Vehicle


class VehicleListView(RoleRequiredMixin, ListView):
    template_name = "admin/vehicles.html"
    context_object_name = "vehicles"
    model = Vehicle
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)


class VehicleCreateView(RoleRequiredMixin, CreateView):
    template_name = "admin/form.html"
    form_class = VehicleForm
    model = Vehicle
    success_url = reverse_lazy("vehicles:list")
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def form_valid(self, form):
        messages.success(self.request, "Vehicle saved successfully.")
        return super().form_valid(form)


class VehicleUpdateView(VehicleCreateView, UpdateView):
    pass
