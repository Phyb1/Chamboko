"""Reusable Signpost website settings."""
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = config("SECRET_KEY", default="change-me-in-env")
INSTALLED_APPS = ["django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes", "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "apps.core"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware", "whitenoise.middleware.WhiteNoiseMiddleware", "django.contrib.sessions.middleware.SessionMiddleware", "django.middleware.common.CommonMiddleware", "django.middleware.csrf.CsrfViewMiddleware", "django.contrib.auth.middleware.AuthenticationMiddleware", "django.contrib.messages.middleware.MessageMiddleware", "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages","apps.core.context_processors.site_settings"]}}]
WSGI_APPLICATION = "config.wsgi.application"
DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = [{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="en-us"; TIME_ZONE="Africa/Harare"; USE_I18N=True; USE_TZ=True
STATIC_URL=config("STATIC_URL",default="/static/"); STATIC_ROOT=BASE_DIR/"staticfiles"; STATICFILES_DIRS=[BASE_DIR/"static_src"]
MEDIA_URL=config("MEDIA_URL",default="/media/"); MEDIA_ROOT=BASE_DIR/"media"
STORAGES={"default":{"BACKEND":"django.core.files.storage.FileSystemStorage"},"staticfiles":{"BACKEND":"whitenoise.storage.CompressedManifestStaticFilesStorage"}}
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
DEBUG=config("DEBUG",default=False,cast=bool); ALLOWED_HOSTS=config("ALLOWED_HOSTS",default="",cast=Csv()); CSRF_TRUSTED_ORIGINS=config("CSRF_TRUSTED_ORIGINS",default="",cast=Csv())
SECURE_SSL_REDIRECT=config("SECURE_SSL_REDIRECT",default=True,cast=bool); SESSION_COOKIE_SECURE=not DEBUG; CSRF_COOKIE_SECURE=not DEBUG; SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")
SITE_NAME=config("SITE_NAME",default="Your Business Name"); TAGLINE=config("TAGLINE",default="Professional services you can trust.")
HERO_TITLE=config("HERO_TITLE",default="Get the service you need, without the hassle."); HERO_TEXT=config("HERO_TEXT",default="Tell customers what you do, where you are and how they can reach you.")
ABOUT_TITLE=config("ABOUT_TITLE",default="About Your Business"); ABOUT_TEXT=config("ABOUT_TEXT",default="Add a short, clear description of your business here."); META_DESCRIPTION=config("META_DESCRIPTION",default="Professional services from Your Business Name.")
WHATSAPP_ORDER_NUMBER=config("WHATSAPP_ORDER_NUMBER",default="263771234567"); BUSINESS_PHONE_DISPLAY=config("BUSINESS_PHONE_DISPLAY",default="+263 77 123 4567"); BUSINESS_EMAIL=config("BUSINESS_EMAIL",default="hello@example.co.zw"); BUSINESS_ADDRESS=config("BUSINESS_ADDRESS",default="Your street address, City, Zimbabwe"); OPENING_HOURS=config("OPENING_HOURS",default="Mon–Sat: 8:00 AM–5:00 PM")
FACEBOOK_URL=config("FACEBOOK_URL",default=""); INSTAGRAM_URL=config("INSTAGRAM_URL",default="")
BRAND_PRIMARY=config("BRAND_PRIMARY",default="#12A8E0"); BRAND_DARK=config("BRAND_DARK",default="#071C2C"); BRAND_LIGHT=config("BRAND_LIGHT",default="#F5FBFE")
LOGO_IMAGE=config("LOGO_IMAGE",default="images/brand/logo-placeholder.svg"); HERO_IMAGE=config("HERO_IMAGE",default="images/hero-placeholder.svg")
SERVICES_JSON=config("SERVICES_JSON",default="[]"); BRANCHES_JSON=config("BRANCHES_JSON",default="[]")
# Quote requests are always saved to the database. Email is a convenience on top, so the
# default backend only prints to the console until real SMTP details are set in .env.
QUOTE_NOTIFY_EMAIL=config("QUOTE_NOTIFY_EMAIL",default="")
DEFAULT_FROM_EMAIL=config("DEFAULT_FROM_EMAIL",default="noreply@localhost")
EMAIL_BACKEND=config("EMAIL_BACKEND",default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST=config("EMAIL_HOST",default="localhost"); EMAIL_PORT=config("EMAIL_PORT",default=25,cast=int)
EMAIL_HOST_USER=config("EMAIL_HOST_USER",default=""); EMAIL_HOST_PASSWORD=config("EMAIL_HOST_PASSWORD",default="")
EMAIL_USE_SSL=config("EMAIL_USE_SSL",default=False,cast=bool); EMAIL_USE_TLS=config("EMAIL_USE_TLS",default=False,cast=bool)
EMAIL_TIMEOUT=10
(BASE_DIR/"logs").mkdir(exist_ok=True)
LOGGING={"version":1,"disable_existing_loggers":False,"handlers":{"file":{"level":"WARNING","class":"logging.FileHandler","filename":BASE_DIR/"logs"/"django.log"}},"root":{"handlers":["file"],"level":"WARNING"}}
