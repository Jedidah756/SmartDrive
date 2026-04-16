from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User

from .forms import ScheduleForm
from .models import Schedule


class ScheduleListView(RoleRequiredMixin, ListView):
    template_name = "admin/schedules.html"
    context_object_name = "schedules"
    model = Schedule
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)


class ScheduleCreateView(RoleRequiredMixin, CreateView):
    template_name = "admin/form.html"
    form_class = ScheduleForm
    model = Schedule
    success_url = reverse_lazy("schedules:list")
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def form_valid(self, form):
        messages.success(self.request, "Schedule saved successfully.")
        return super().form_valid(form)


class ScheduleUpdateView(ScheduleCreateView, UpdateView):
    pass
