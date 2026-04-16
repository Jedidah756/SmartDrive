from django import forms

from .models import Route


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ["name", "start_point", "end_point", "stops_json", "distance_km"]
        widgets = {
            "stops_json": forms.Textarea(attrs={"placeholder": '[{"name": "Main Gate", "lat": -1.0, "lng": 36.8}]'}),
        }
