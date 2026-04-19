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
            ("KDA-103C", "Nissan Civilian", 28, Vehicle.Status.ACTIVE),
            ("KMC-001M", "Bajaj RE Motorbike", 3, Vehicle.Status.ACTIVE),
            ("KMC-002M", "TVS King Motorbike", 3, Vehicle.Status.ACTIVE),
            ("KMC-003M", "Piaggio Ape Motorbike", 4, Vehicle.Status.ACTIVE),
        ]
        vehicles = []
        for plate, model, capacity, status in vehicle_rows:
            vehicle, _ = Vehicle.objects.get_or_create(
                plate_number=plate,
                defaults={"model": model, "capacity": capacity, "status": status},
            )
            vehicles.append(vehicle)

        route_rows = [
            ("Eldoret Express", "Eldoret", "Kapsabet", Decimal("35.00"), [{"name": "Eldoret", "lat": 0.5171, "lng": 35.2909}, {"name": "Mosoriot", "lat": 0.4000, "lng": 35.2000}, {"name": "Lessos", "lat": 0.3000, "lng": 35.1000}, {"name": "Kapsabet", "lat": 0.2083, "lng": 35.0050}]),
            ("Nandi Hills Shuttle", "Kapsabet", "Nandi Hills", Decimal("25.00"), [{"name": "Kapsabet", "lat": 0.2083, "lng": 35.0050}, {"name": "Kabiyet", "lat": 0.1900, "lng": 35.0200}, {"name": "Namgoi", "lat": 0.1800, "lng": 34.9900}, {"name": "Nandi Hills", "lat": 0.1333, "lng": 35.1833}]),
            ("Baraton University Line", "Kapsabet", "Baraton", Decimal("15.00"), [{"name": "Kapsabet", "lat": 0.2083, "lng": 35.0050}, {"name": "Chepterit", "lat": 0.2300, "lng": 35.0300}, {"name": "Kapkangani", "lat": 0.2200, "lng": 35.0500}, {"name": "Baraton", "lat": 0.2400, "lng": 35.0700}]),
            ("Kaiboi Tech Route", "Kapsabet", "Kaiboi", Decimal("20.00"), [{"name": "Kapsabet", "lat": 0.2083, "lng": 35.0050}, {"name": "Kilibwoni", "lat": 0.1950, "lng": 34.9800}, {"name": "Ol'Lessos", "lat": 0.1850, "lng": 35.0100}, {"name": "Kaiboi", "lat": 0.1700, "lng": 35.0400}]),
            ("Motorbike Quick Link", "Eldoret", "Mosoriot", Decimal("18.00"), [{"name": "Eldoret", "lat": 0.5171, "lng": 35.2909}, {"name": "Mugundoi", "lat": 0.4600, "lng": 35.2500}, {"name": "Mosoriot", "lat": 0.4000, "lng": 35.2000}]),
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
                defaults={"days_of_week": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]},
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
