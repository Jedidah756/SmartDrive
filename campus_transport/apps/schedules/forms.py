from django import forms

from apps.accounts.models import User

from .models import Schedule


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ["route", "vehicle", "driver", "departure_time", "days_of_week", "status"]
        widgets = {
            "days_of_week": forms.Textarea(attrs={"placeholder": '["monday", "tuesday", "wednesday"]'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["driver"].queryset = User.objects.filter(role=User.Role.DRIVER)
