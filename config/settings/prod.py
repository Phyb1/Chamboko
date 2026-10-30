from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa

DEBUG = False

if SECRET_KEY == "change-me-in-env":  # noqa: F405
    raise ImproperlyConfigured("Set a real SECRET_KEY in the .env file before running in production.")
