from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User
from apps.trips.models import Trip

from .forms import IncidentForm
from .models import Incident


class IncidentListView(RoleRequiredMixin, ListView):
    context_object_name = "incidents"
    allowed_roles = (User.Role.DRIVER, User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def get_template_names(self):
        if self.request.user.is_driver:
            return ["driver/incidents.html"]
        return ["admin/incidents.html"]

    def get_queryset(self):
        queryset = Incident.objects.select_related("trip__schedule__route", "driver")
        if self.request.user.is_driver:
            return queryset.filter(driver=self.request.user)
        return queryset


class IncidentCreateView(RoleRequiredMixin, CreateView):
    template_name = "driver/incident_form.html"
    form_class = IncidentForm
    success_url = reverse_lazy("incidents:list")
    allowed_roles = (User.Role.DRIVER,)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["trip"].queryset = Trip.objects.filter(driver=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.driver = self.request.user
        messages.success(self.request, "Incident report recorded.")
        return super().form_valid(form)
