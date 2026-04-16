import json

from django.contrib import messages
from django.http import JsonResponse
from django.views import View
from django.views.generic import FormView

from apps.accounts.mixins import RoleRequiredMixin
from apps.accounts.models import User

from .forms import ReportFilterForm
from .models import Report
from .services import build_report_payload, export_report_csv, export_report_pdf


class ReportsDashboardView(RoleRequiredMixin, FormView):
    template_name = "reports/dashboard.html"
    form_class = ReportFilterForm
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reports"] = Report.objects.select_related("generated_by")
        context["payload"] = None
        context["chart_data_json"] = json.dumps({})
        return context

    def form_valid(self, form):
        report = Report.objects.create(
            report_type=form.cleaned_data["report_type"],
            date_range_start=form.cleaned_data["date_range_start"],
            date_range_end=form.cleaned_data["date_range_end"],
            generated_by=self.request.user,
        )
        payload = build_report_payload(report.date_range_start, report.date_range_end)
        if form.cleaned_data["export_format"] == "csv":
            return export_report_csv(payload)
        messages.success(self.request, "PDF report generated successfully.")
        return export_report_pdf(payload)


class ReportsApiView(RoleRequiredMixin, View):
    allowed_roles = (User.Role.TRANSPORT_ADMIN, User.Role.SUPER_ADMIN)

    def get(self, request):
        form = ReportFilterForm(request.GET)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)
        payload = build_report_payload(form.cleaned_data["date_range_start"], form.cleaned_data["date_range_end"])
        return JsonResponse(payload)
