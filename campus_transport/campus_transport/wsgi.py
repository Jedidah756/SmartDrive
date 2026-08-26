import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campus_transport.settings")

_django_application = get_wsgi_application()

def application(environ, start_response):
	host = environ.get("HTTP_HOST")
	try:
		# Write the raw Host header to stdout so deployment logs capture it
		import sys
		print(f"WSGI_HTTP_HOST: {host}")
		sys.stdout.flush()
	except Exception:
		pass
	return _django_application(environ, start_response)
