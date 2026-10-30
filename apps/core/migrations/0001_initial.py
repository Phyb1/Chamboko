from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def seed_from_env(apps, schema_editor):
    import json
    SiteProfile = apps.get_model("core", "SiteProfile")
    Service = apps.get_model("core", "Service")
    Branch = apps.get_model("core", "Branch")

    if not SiteProfile.objects.exists():
        SiteProfile.objects.create(
            site_name=settings.SITE_NAME, tagline=settings.TAGLINE,
            hero_title=settings.HERO_TITLE, hero_text=settings.HERO_TEXT,
            about_title=settings.ABOUT_TITLE, about_text=settings.ABOUT_TEXT,
            meta_description=settings.META_DESCRIPTION,
            phone=settings.BUSINESS_PHONE_DISPLAY, email=settings.BUSINESS_EMAIL,
            whatsapp_number=settings.WHATSAPP_ORDER_NUMBER,
            address=settings.BUSINESS_ADDRESS, opening_hours=settings.OPENING_HOURS,
            facebook_url=settings.FACEBOOK_URL, instagram_url=settings.INSTAGRAM_URL,
            brand_primary=settings.BRAND_PRIMARY, brand_dark=settings.BRAND_DARK,
            brand_light=settings.BRAND_LIGHT, logo_image=settings.LOGO_IMAGE,
            hero_image=settings.HERO_IMAGE,
        )

    try:
        services = json.loads(settings.SERVICES_JSON or "[]")
    except (TypeError, ValueError):
        services = []
    for i, item in enumerate(services):
        if isinstance(item, dict) and item.get("name"):
            Service.objects.get_or_create(
                name=item["name"],
                defaults={
                    "description": item.get("description", ""),
                    "icon": item.get("icon", "✦"),
                    "sort_order": i,
                },
            )

    try:
        branches = json.loads(settings.BRANCHES_JSON or "[]")
    except (TypeError, ValueError):
        branches = []
    for i, item in enumerate(branches):
        if isinstance(item, dict) and item.get("name"):
            Branch.objects.get_or_create(
                name=item["name"],
                defaults={
                    "address": item.get("address", ""),
                    "phone": item.get("phone", ""),
                    "whatsapp_number": item.get("whatsapp_number", ""),
                    "latitude": item.get("latitude") or None,
                    "longitude": item.get("longitude") or None,
                    "google_place_id": item.get("google_place_id", ""),
                    "sort_order": i,
                },
            )


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Branch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=255)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("whatsapp_number", models.CharField(blank=True, max_length=30)),
                ("latitude", models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ("longitude", models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ("google_place_id", models.CharField(blank=True, max_length=255)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("sort_order", "name")},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("icon", models.CharField(blank=True, default="✦", max_length=20)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("sort_order", "name")},
        ),
        migrations.CreateModel(
            name="SiteProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("site_name", models.CharField(default="Your Business Name", max_length=120)),
                ("tagline", models.CharField(default="Professional services you can trust.", max_length=180)),
                ("hero_title", models.CharField(default="Get the service you need, without the hassle.", max_length=220)),
                ("hero_text", models.TextField(default="Tell customers what you do, where you are and how they can reach you.")),
                ("about_title", models.CharField(default="About Your Business", max_length=180)),
                ("about_text", models.TextField(default="Add a short, clear description of your business here.")),
                ("meta_description", models.CharField(default="Professional services from Your Business Name.", max_length=180)),
                ("phone", models.CharField(blank=True, max_length=40)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("whatsapp_number", models.CharField(blank=True, max_length=30)),
                ("address", models.CharField(blank=True, max_length=255)),
                ("opening_hours", models.CharField(blank=True, max_length=180)),
                ("facebook_url", models.URLField(blank=True)),
                ("instagram_url", models.URLField(blank=True)),
                ("brand_primary", models.CharField(default="#12A8E0", max_length=30)),
                ("brand_dark", models.CharField(default="#071C2C", max_length=30)),
                ("brand_light", models.CharField(default="#F5FBFE", max_length=30)),
                ("logo_image", models.CharField(default="images/brand/logo-placeholder.svg", max_length=255)),
                ("hero_image", models.CharField(default="images/hero-placeholder.svg", max_length=255)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Site & contact information", "verbose_name_plural": "Site & contact information"},
        ),
        migrations.CreateModel(
            name="SiteEvent",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_type", models.CharField(choices=[("whatsapp", "WhatsApp"), ("directions", "Directions"), ("phone", "Phone"), ("email", "Email"), ("service", "Service enquiry"), ("navigation", "Navigation"), ("other", "Other")], max_length=30)),
                ("label", models.CharField(blank=True, max_length=120)),
                ("page", models.CharField(blank=True, max_length=255)),
                ("target", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("branch", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="events", to="core.branch")),
                ("service", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="events", to="core.service")),
            ],
            options={"ordering": ("-created_at",), "indexes": [models.Index(fields=("event_type", "created_at"), name="core_siteev_event_ti_8c3f0a_idx")]},
        ),
        migrations.RunPython(seed_from_env, migrations.RunPython.noop),
    ]
