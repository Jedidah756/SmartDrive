from django.views.generic import ListView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User

from .models import SmsNotification


class SmsLogView(RoleRequiredMixin, ListView):
    template_name = "admin/sms_log.html"
    context_object_name = "notifications"
    paginate_by = 30
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def get_queryset(self):
        return SmsNotification.objects.select_related("recipient", "trip__schedule__route")


class StudentSmsInboxView(RoleRequiredMixin, ListView):
    template_name = "student/sms_inbox.html"
    context_object_name = "notifications"
    paginate_by = 20
    allowed_roles = (User.Role.STUDENT,)

    def get_queryset(self):
        return SmsNotification.objects.filter(
            recipient=self.request.user
        ).select_related("trip__schedule__route")
