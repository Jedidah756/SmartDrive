from django import forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["trip", "rating", "comment"]


class FeedbackResponseForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["admin_response"]
