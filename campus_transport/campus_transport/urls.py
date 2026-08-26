from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", include(("apps.accounts.urls", "accounts"), namespace="accounts")),
    path("vehicles/", include(("apps.vehicles.urls", "vehicles"), namespace="vehicles")),
    path("routes/", include(("apps.routes.urls", "routes"), namespace="routes")),
    path("schedules/", include(("apps.schedules.urls", "schedules"), namespace="schedules")),
    path("trips/", include(("apps.trips.urls", "trips"), namespace="trips")),
    path("bookings/", include(("apps.bookings.urls", "bookings"), namespace="bookings")),
    path("feedback/", include(("apps.feedback.urls", "feedback"), namespace="feedback")),
    path("incidents/", include(("apps.incidents.urls", "incidents"), namespace="incidents")),
    path("reports/", include(("apps.reports.urls", "reports"), namespace="reports")),
    path("notifications/", include(("apps.notifications.urls", "notifications"), namespace="notifications")),
    path("driver/", include(("apps.driver.urls", "driver"), namespace="driver")),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
