import csv
from io import BytesIO, StringIO

from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from apps.feedback.models import Feedback
from apps.incidents.models import Incident
from apps.trips.models import Trip


def build_report_payload(start_date, end_date):
    trips = Trip.objects.filter(trip_date__range=(start_date, end_date)).select_related("schedule__route", "driver")
    return {
        "total_trips": trips.count(),
        "completed_trips": trips.filter(status=Trip.Status.ARRIVED).count(),
        "delayed_trips": trips.filter(status=Trip.Status.DELAYED).count(),
        "incident_count": Incident.objects.filter(reported_at__date__range=(start_date, end_date)).count(),
        "route_utilization": list(trips.values("schedule__route__name").annotate(total=Count("id")).order_by("-total")[:6]),
        "driver_performance": list(
            trips.values("driver__name")
            .annotate(total=Count("id"), arrived=Count("id", filter=Q(status=Trip.Status.ARRIVED)))
            .order_by("-arrived")[:6]
        ),
        "ratings": list(
            Feedback.objects.filter(created_at__date__range=(start_date, end_date))
            .values("trip__schedule__route__name")
            .annotate(avg_rating=Avg("rating"), total=Count("id"))
            .order_by("-avg_rating")[:6]
        ),
    }


def export_report_csv(payload):
    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow(["Metric", "Value"])
    writer.writerow(["Total Trips", payload["total_trips"]])
    writer.writerow(["Completed Trips", payload["completed_trips"]])
    writer.writerow(["Delayed Trips", payload["delayed_trips"]])
    writer.writerow(["Incident Count", payload["incident_count"]])
    response = HttpResponse(stream.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="transport-report.csv"'
    return response


def export_report_pdf(payload):
    stream = BytesIO()
    pdf = canvas.Canvas(stream, pagesize=A4)
    pdf.setTitle("Transport Report")
    text = pdf.beginText(40, 800)
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Campus Transport Report")
    text.setFont("Helvetica", 11)
    for label, value in [
        ("Total Trips", payload["total_trips"]),
        ("Completed Trips", payload["completed_trips"]),
        ("Delayed Trips", payload["delayed_trips"]),
        ("Incident Count", payload["incident_count"]),
    ]:
        text.textLine(f"{label}: {value}")
    pdf.drawText(text)
    pdf.showPage()
    pdf.save()
    response = HttpResponse(stream.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="transport-report.pdf"'
    return response
