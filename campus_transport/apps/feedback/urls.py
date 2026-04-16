from django.urls import path

from .views import FeedbackCreateView, FeedbackListView, FeedbackRespondView

urlpatterns = [
    path("", FeedbackListView.as_view(), name="list"),
    path("create/", FeedbackCreateView.as_view(), name="create"),
    path("<int:pk>/respond/", FeedbackRespondView.as_view(), name="respond"),
]
