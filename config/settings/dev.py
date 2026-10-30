from .base import *  # noqa
DEBUG=True
ALLOWED_HOSTS=["127.0.0.1","localhost"]
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
# The manifest storage used in production needs `collectstatic` first; plain storage lets
# tests and `runserver` render pages without it.
STORAGES = {**STORAGES, "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}}
