from decimal import Decimal
from types import SimpleNamespace

import pytest

from apps.core.models import Branch, Package, Service, SiteProfile


@pytest.fixture
def site(db):
    """A small test site.

    The first migration seeds a default SiteProfile and only one is allowed, so the tests
    update that record instead of trying to add a second.
    """
    # Sample services/branches can also be seeded from .env, so start from a clean slate.
    Service.objects.all().delete()
    Branch.objects.all().delete()
    Package.objects.all().delete()

    profile = SiteProfile.objects.first() or SiteProfile()
    profile.site_name = "Test Business"
    profile.tagline = "Test tagline"
    profile.about_title = "About Test Business"
    profile.about_text = "First paragraph.\n\nSecond paragraph."
    profile.whatsapp_number = "263712345678"
    profile.phone = "+263 71 234 5678"
    profile.email = "test@example.com"
    profile.address = "1 Test Road"
    profile.opening_hours = ""
    profile.save()

    service = Service.objects.create(name="Test Service", description="A useful service.")
    branch = Branch.objects.create(
        name="Test Branch", address="1 Test Road", latitude="-19.4550000", longitude="29.8170000"
    )
    package = Package.objects.create(
        name="Test Package",
        price=Decimal("1200.00"),
        summary="A test package.",
        includes="• Inverter\n\n- Battery\n",
        runs="Fridge\nLights",
    )
    return SimpleNamespace(profile=profile, service=service, branch=branch, package=package)
