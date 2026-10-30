from .site_data import branches, packages, profile, services
from .whatsapp import whatsapp_link


def site_settings(request):
    p = profile()
    get = lambda name, default="": getattr(p, name, default) if hasattr(p, name) else p.get(name, default)
    return {
        "SITE_NAME": get("site_name"),
        "TAGLINE": get("tagline"),
        "HERO_TITLE": get("hero_title"),
        "HERO_TEXT": get("hero_text"),
        "ABOUT_TITLE": get("about_title"),
        "ABOUT_TEXT": get("about_text"),
        "META_DESCRIPTION": get("meta_description"),
        "WHATSAPP_ORDER_NUMBER": get("whatsapp_number"),
        "WHATSAPP_LINK": whatsapp_link(get("whatsapp_number") or None),
        "BUSINESS_PHONE_DISPLAY": get("phone"),
        "BUSINESS_EMAIL": get("email"),
        "BUSINESS_ADDRESS": get("address"),
        "OPENING_HOURS": get("opening_hours"),
        "FACEBOOK_URL": get("facebook_url"),
        "INSTAGRAM_URL": get("instagram_url"),
        "BRAND_PRIMARY": get("brand_primary"),
        "BRAND_DARK": get("brand_dark"),
        "BRAND_LIGHT": get("brand_light"),
        "LOGO_IMAGE": get("logo_image"),
        "HERO_IMAGE": get("hero_image"),
        "SERVICES": services(),
        "PACKAGES": packages(),
        "BRANCHES": branches(),
    }
