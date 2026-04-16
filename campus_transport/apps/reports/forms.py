from django import forms

from .models import Report


class ReportFilterForm(forms.Form):
    report_type = forms.ChoiceField(choices=Report.Type.choices)
    date_range_start = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    date_range_end = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    export_format = forms.ChoiceField(choices=[("pdf", "PDF"), ("csv", "CSV")])
