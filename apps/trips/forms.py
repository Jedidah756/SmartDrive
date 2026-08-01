from django import forms

from .models import TripUpdate


class TripUpdateForm(forms.ModelForm):
    class Meta:
        model = TripUpdate
        fields = ["status", "note", "latitude", "longitude"]
