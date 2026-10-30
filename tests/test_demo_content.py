from decimal import Decimal

import pytest
from django.core.management import call_command

from apps.core.models import Package, Service, SiteProfile

SERVICE_NAMES = {
    "System Design & Installation", "Energy Audits", "Maintenance & Repair",
    "Water Pumping Systems", "System Upgrades", "Consultation & Advisory",
}


@pytest.fixture
def demo(db):
    call_command("loaddata", "chamboko_demo", verbosity=0)


def test_demo_content_replaces_the_seeded_profile(demo):
    assert SiteProfile.objects.count() == 1
    profile = SiteProfile.objects.get()
    assert profile.site_name == "Chamboko Solar Technology"
    assert profile.whatsapp_number == "263710955403"
    assert profile.logo_image == "images/brand/logo.png"


def test_demo_content_has_the_six_services(demo):
    assert SERVICE_NAMES <= set(Service.objects.values_list("name", flat=True))


def test_demo_packages_match_the_client_flyers(demo):
    small = Package.objects.get(name="3.3 KVA SRNE Package")
    large = Package.objects.get(name="6.2 KVA Package")
    assert small.price == Decimal("1200.00")
    assert large.price == Decimal("2200.00")
    assert "Free installation" in small.includes_list()
    assert large.badge == "Christmas special"


def test_demo_site_renders(client, demo):
    page = client.get("/").content.decode()
    for expected in ("Chamboko Solar Technology", "3.3 KVA SRNE Package", "$1,200", "$2,200", "Christmas special"):
        assert expected in page


def test_every_page_renders_with_the_demo_content(client, demo):
    for url in ("/", "/services/", "/about/", "/contact/"):
        assert client.get(url).status_code == 200, url
