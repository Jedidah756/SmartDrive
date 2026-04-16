from datetime import date

from apps.trips.models import Trip

from .models import Schedule


def ensure_daily_trips(target_date=None):
    target_date = target_date or date.today()
    weekday = target_date.strftime("%A").lower()
    schedules = Schedule.objects.filter(status=Schedule.Status.ACTIVE)
    for schedule in schedules:
        # A lightweight scheduler for local demos: create today's trip only when a matching recurring schedule applies.
        if weekday in [day.lower() for day in schedule.days_of_week]:
            Trip.objects.get_or_create(
                schedule=schedule,
                trip_date=target_date,
                defaults={
                    "driver": schedule.driver,
                    "status": Trip.Status.SCHEDULED,
                    "scheduled_departure": schedule.departure_time,
                },
            )
    return target_date
