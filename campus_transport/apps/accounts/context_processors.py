from django.conf import settings


def platform_settings(request):
    return {
        "institution_name": settings.INSTITUTION_NAME,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }
