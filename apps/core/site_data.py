from urllib.parse import urlencode
from django.conf import settings
from .models import Branch, Package, Service, SiteProfile


def _env_profile():
    return {
        "site_name": settings.SITE_NAME,
        "tagline": settings.TAGLINE,
        "hero_title": settings.HERO_TITLE,
        "hero_text": settings.HERO_TEXT,
        "about_title": settings.ABOUT_TITLE,
        "about_text": settings.ABOUT_TEXT,
        "meta_description": settings.META_DESCRIPTION,
        "phone": settings.BUSINESS_PHONE_DISPLAY,
        "email": settings.BUSINESS_EMAIL,
        "whatsapp_number": settings.WHATSAPP_ORDER_NUMBER,
        "address": settings.BUSINESS_ADDRESS,
        "opening_hours": settings.OPENING_HOURS,
        "facebook_url": settings.FACEBOOK_URL,
        "instagram_url": settings.INSTAGRAM_URL,
        "brand_primary": settings.BRAND_PRIMARY,
        "brand_dark": settings.BRAND_DARK,
        "brand_light": settings.BRAND_LIGHT,
        "logo_image": settings.LOGO_IMAGE,
        "hero_image": settings.HERO_IMAGE,
    }


def profile():
    obj = SiteProfile.objects.first()
    return obj or _env_profile()


def profile_value(name, default=""):
    """Read one field from the editable profile, falling back to the .env defaults."""
    p = profile()
    if isinstance(p, dict):
        return p.get(name, default)
    return getattr(p, name, default)


def _directions_url(branch):
    place_id = str(getattr(branch, "google_place_id", "") or "").strip()
    lat = str(getattr(branch, "latitude", "") or "").strip()
    lng = str(getattr(branch, "longitude", "") or "").strip()
    address = str(getattr(branch, "address", "") or "").strip()
    name = str(getattr(branch, "name", "") or "").strip()
    destination = address or name
    params = {"api": "1", "destination": destination, "travelmode": "driving"}
    if place_id:
        params["destination_place_id"] = place_id
    elif lat and lng:
        params["destination"] = f"{lat},{lng}"
    return "https://www.google.com/maps/dir/?" + urlencode(params)


def services():
    if Service.objects.exists():
        return Service.objects.filter(is_active=True)
    return []


def packages():
    return Package.objects.filter(is_active=True)


def branches():
    return [
        {
            "object": branch,
            "name": branch.name,
            "address": branch.address,
            "phone": branch.phone,
            "whatsapp_number": branch.whatsapp_number,
            "directions_url": _directions_url(branch),
        }
        for branch in Branch.objects.filter(is_active=True)
    ]
