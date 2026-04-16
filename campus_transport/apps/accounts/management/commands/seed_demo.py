from datetime import date, time, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.bookings.models import Booking
from apps.feedback.models import Feedback
from apps.incidents.models import Incident
from apps.reports.models import Report
from apps.routes.models import Route
from apps.schedules.models import Schedule
from apps.trips.models import Trip, TripUpdate
from apps.vehicles.models import Vehicle


class Command(BaseCommand):
    help = "Seed demo data for the campus transport project."

    def handle(self, *args, **options):
        User = get_user_model()

        users = [
            {"email": "superadmin@demo.local", "name": "System Super Admin", "role": User.Role.SUPER_ADMIN, "employee_id": "SA-001", "is_staff": True, "is_superuser": True},
            {"email": "admin@demo.local", "name": "Transit Operations Admin", "role": User.Role.TRANSPORT_ADMIN, "employee_id": "TA-101", "is_staff": True},
            {"email": "driver1@demo.local", "name": "Daniel Mwangi", "role": User.Role.DRIVER, "employee_id": "DRV-201"},
            {"email": "driver2@demo.local", "name": "Grace Wanjiru", "role": User.Role.DRIVER, "employee_id": "DRV-202"},
            {"email": "student1@demo.local", "name": "Amina Noor", "role": User.Role.STUDENT, "student_id": "ST-1001"},
            {"email": "student2@demo.local", "name": "Brian Otieno", "role": User.Role.STUDENT, "student_id": "ST-1002"},
            {"email": "student3@demo.local", "name": "Cynthia Maina", "role": User.Role.STUDENT, "student_id": "ST-1003"},
        ]
        created_users = {}
        for payload in users:
            email = payload.pop("email")
            user, created = User.objects.get_or_create(email=email, defaults=payload)
            if created:
                user.set_password("DemoPass123!")
                user.save()
            created_users[email] = user

        vehicle_rows = [
            ("KDA-101A", "Toyota Coaster", 32, Vehicle.Status.ACTIVE),
            ("KDA-102B", "Isuzu FRR", 45, Vehicle.Status.ACTIVE),
            ("KDA-103C", "Nissan Civilian", 28, Vehicle.Status.MAINTENANCE),
            ("KDA-104D", "Mitsubishi Rosa", 30, Vehicle.Status.ACTIVE),
            ("KDA-105E", "Hyundai County", 29, Vehicle.Status.INACTIVE),
        ]
        vehicles = []
        for plate, model, capacity, status in vehicle_rows:
            vehicle, _ = Vehicle.objects.get_or_create(
                plate_number=plate,
                defaults={"model": model, "capacity": capacity, "status": status},
            )
            vehicles.append(vehicle)

        route_rows = [
            ("Main Campus Loop", "Main Gate", "Library", Decimal("4.20"), [{"name": "Main Gate", "lat": -1.286389, "lng": 36.817223}, {"name": "Science Block", "lat": -1.284900, "lng": 36.819300}, {"name": "Library", "lat": -1.283500, "lng": 36.821000}]),
            ("Hostels Express", "North Hostels", "Main Campus", Decimal("6.80"), [{"name": "North Hostels", "lat": -1.290500, "lng": 36.812500}, {"name": "Sports Complex", "lat": -1.288000, "lng": 36.815900}, {"name": "Main Campus", "lat": -1.286389, "lng": 36.817223}]),
            ("Westlands Shuttle", "Westlands", "Main Campus", Decimal("11.50"), [{"name": "Westlands", "lat": -1.267600, "lng": 36.810800}, {"name": "Museum Hill", "lat": -1.273800, "lng": 36.813900}, {"name": "Main Campus", "lat": -1.286389, "lng": 36.817223}]),
            ("CBD Connector", "CBD Terminal", "Main Campus", Decimal("8.40"), [{"name": "CBD Terminal", "lat": -1.286000, "lng": 36.821900}, {"name": "Haile Selassie", "lat": -1.285200, "lng": 36.824900}, {"name": "Main Campus", "lat": -1.286389, "lng": 36.817223}]),
            ("Karen Route", "Karen Centre", "Main Campus", Decimal("14.30"), [{"name": "Karen Centre", "lat": -1.319700, "lng": 36.706400}, {"name": "Langata Road", "lat": -1.309100, "lng": 36.776800}, {"name": "Main Campus", "lat": -1.286389, "lng": 36.817223}]),
        ]
        routes = []
        for name, start, end, distance, stops in route_rows:
            route, _ = Route.objects.get_or_create(
                name=name,
                defaults={
                    "start_point": start,
                    "end_point": end,
                    "distance_km": distance,
                    "stops_json": stops,
                },
            )
            routes.append(route)

        drivers = [created_users["driver1@demo.local"], created_users["driver2@demo.local"]]
        schedules = []
        for index, route in enumerate(routes):
            schedule, _ = Schedule.objects.get_or_create(
                route=route,
                vehicle=vehicles[index % len(vehicles)],
                driver=drivers[index % len(drivers)],
                departure_time=time(7 + index, 0),
                defaults={"days_of_week": ["monday", "tuesday", "wednesday", "thursday", "friday"]},
            )
            schedules.append(schedule)

        base_date = date.today()
        students = [created_users["student1@demo.local"], created_users["student2@demo.local"], created_users["student3@demo.local"]]

        for index, schedule in enumerate(schedules[:5]):
            trip, _ = Trip.objects.get_or_create(
                schedule=schedule,
                trip_date=base_date - timedelta(days=index),
                defaults={
                    "scheduled_departure": schedule.departure_time,
                    "driver": schedule.driver,
                    "status": Trip.Status.ARRIVED if index % 2 == 0 else Trip.Status.DELAYED,
                },
            )
            TripUpdate.objects.get_or_create(
                trip=trip,
                status=Trip.Status.DEPARTED,
                note="Departed from origin stop.",
                latitude=-1.286389 + (index * 0.002),
                longitude=36.817223 + (index * 0.003),
            )
            TripUpdate.objects.get_or_create(
                trip=trip,
                status=trip.status,
                note="Current status snapshot.",
                latitude=-1.285389 + (index * 0.002),
                longitude=36.818223 + (index * 0.003),
            )
            Booking.objects.get_or_create(
                student=students[index % len(students)],
                trip=trip,
                seat_number=index + 1,
                defaults={"status": Booking.Status.RESERVED},
            )
            Feedback.objects.get_or_create(
                student=students[index % len(students)],
                trip=trip,
                defaults={
                    "rating": 4 + (index % 2),
                    "comment": "Comfortable trip with clear stop announcements.",
                    "admin_response": "Thank you for the feedback.",
                },
            )
            Incident.objects.get_or_create(
                trip=trip,
                driver=trip.driver,
                description=f"Demo incident log {index + 1}.",
                defaults={"severity": Incident.Severity.MEDIUM if index % 2 else Incident.Severity.LOW},
            )

        for report_type in Report.Type.values:
            Report.objects.get_or_create(
                report_type=report_type,
                date_range_start=base_date - timedelta(days=30),
                date_range_end=base_date,
                generated_by=created_users["admin@demo.local"],
            )

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
