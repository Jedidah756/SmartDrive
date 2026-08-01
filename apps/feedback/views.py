from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User
from apps.trips.models import Trip

from .forms import FeedbackForm, FeedbackResponseForm
from .models import Feedback


class FeedbackListView(RoleRequiredMixin, ListView):
    allowed_roles = (User.Role.STUDENT, User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def get_template_names(self):
        if self.request.user.is_student:
            return ["student/feedback.html"]
        return ["admin/feedback.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_student:
            context["trip_options"] = Trip.objects.filter(bookings__student=self.request.user).distinct()
        return context

    def get_queryset(self):
        queryset = Feedback.objects.select_related("student", "trip__schedule__route")
        if self.request.user.is_student:
            return queryset.filter(student=self.request.user)
        return queryset


class FeedbackCreateView(RoleRequiredMixin, CreateView):
    template_name = "student/feedback_form.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("feedback:list")
    allowed_roles = (User.Role.STUDENT,)

    def form_valid(self, form):
        form.instance.student = self.request.user
        messages.success(self.request, "Feedback submitted successfully.")
        return super().form_valid(form)


class FeedbackRespondView(RoleRequiredMixin, UpdateView):
    template_name = "admin/form.html"
    form_class = FeedbackResponseForm
    model = Feedback
    success_url = reverse_lazy("feedback:list")
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def form_valid(self, form):
        messages.success(self.request, "Response saved.")
        return super().form_valid(form)
