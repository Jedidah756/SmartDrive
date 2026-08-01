from django.urls import path

from .views import SmsLogView, StudentSmsInboxView

urlpatterns = [
    path("sms/", SmsLogView.as_view(), name="sms-log"),
    path("inbox/", StudentSmsInboxView.as_view(), name="inbox"),
]
