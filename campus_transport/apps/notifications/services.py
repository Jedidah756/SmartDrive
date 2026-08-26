from apps.bookings.models import Booking

from .models import SmsNotification


TRIGGER_MAP = {
    "departed": SmsNotification.Trigger.TRIP_DEPARTED,
    "delayed": SmsNotification.Trigger.TRIP_DELAYED,
    "cancelled": SmsNotification.Trigger.TRIP_CANCELLED,
    "arrived": SmsNotification.Trigger.TRIP_ARRIVED,
    "breakdown": SmsNotification.Trigger.BREAKDOWN,
}

MESSAGE_TEMPLATES = {
    SmsNotification.Trigger.TRIP_DEPARTED: "Your bus on {route} has departed. Estimated arrival at destination shortly.",
    SmsNotification.Trigger.TRIP_DELAYED: "Alert: Your bus on {route} is delayed. Please check the app for updates.",
    SmsNotification.Trigger.TRIP_CANCELLED: "Alert: Your trip on {route} has been cancelled. Please make alternative arrangements.",
    SmsNotification.Trigger.TRIP_ARRIVED: "Your bus on {route} has arrived at the destination.",
    SmsNotification.Trigger.BREAKDOWN: "Alert: The bus on {route} has reported a breakdown. Transport admin has been notified.",
}

NOTIFY_ON = {
    SmsNotification.Trigger.TRIP_DEPARTED,
    SmsNotification.Trigger.TRIP_DELAYED,
    SmsNotification.Trigger.TRIP_CANCELLED,
    SmsNotification.Trigger.BREAKDOWN,
}


def notify_trip_students(trip, new_status):
    trigger = TRIGGER_MAP.get(new_status)
    if not trigger or trigger not in NOTIFY_ON:
        return 0

    route_name = trip.schedule.route.name
    message = MESSAGE_TEMPLATES[trigger].format(route=route_name)

    students = (
        Booking.objects.filter(trip=trip, status=Booking.Status.RESERVED)
        .select_related("student")
        .values_list("student", flat=True)
        .distinct()
    )

    notifications = [
        SmsNotification(recipient_id=student_id, trip=trip, trigger=trigger, message=message)
        for student_id in students
    ]
    SmsNotification.objects.bulk_create(notifications)
    return len(notifications)
