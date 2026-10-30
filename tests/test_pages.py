from decimal import Decimal

from django.urls import reverse

from apps.core.models import Branch, Package, SiteEvent
from apps.core.site_data import _directions_url


def html(response):
    return response.content.decode()


def test_home_page(client, site):
    response = client.get("/")
    assert response.status_code == 200
    page = html(response)
    for expected in ("Test Business", "Test Service", "Test Package", "$1,200"):
        assert expected in page
    assert f"?package={site.package.pk}" in page


def test_home_page_links_to_the_admin_managed_whatsapp_number(client, site):
    assert "wa.me/263712345678" in html(client.get("/"))


def test_services_page_lists_packages_and_services(client, site):
    page = html(client.get(reverse("core:services")))
    assert "Test Package" in page
    assert "$1,200" in page
    assert "<li>Inverter</li>" in page
    assert "<li>Battery</li>" in page
    assert "<li>Fridge</li>" in page
    assert "Test Service" in page


def test_inactive_packages_are_hidden(client, site):
    Package.objects.create(name="Hidden Package", price=Decimal("5"), is_active=False)
    assert "Hidden Package" not in html(client.get(reverse("core:services")))
    assert "Hidden Package" not in html(client.get("/"))


def test_about_page_splits_paragraphs(client, site):
    page = html(client.get(reverse("core:about")))
    assert "About Test Business" in page
    assert "<p>First paragraph.</p>" in page
    assert "<p>Second paragraph.</p>" in page


def test_contact_page_has_the_quote_form(client, site):
    response = client.get(reverse("core:contact"))
    assert response.status_code == 200
    page = html(response)
    for field in ("name", "phone", "email", "location", "package", "message"):
        assert f'name="{field}"' in page
    assert "csrfmiddlewaretoken" in page


def test_contact_page_hides_empty_opening_hours(client, site):
    assert "Opening hours" not in html(client.get(reverse("core:contact")))


def test_branch_list_only_shows_for_several_branches(client, site):
    assert "Our locations" not in html(client.get(reverse("core:contact")))
    Branch.objects.create(name="Second Branch", address="2 Test Road")
    assert "Our locations" in html(client.get(reverse("core:contact")))


def test_service_partial_uses_the_admin_managed_number(client, site):
    response = client.get(reverse("core:service_detail", args=[site.service.pk]))
    assert response.status_code == 200
    assert "Test Service" in html(response)
    assert "wa.me/263712345678" in html(response)


def test_service_partial_returns_404_for_unknown_service(client, site):
    assert client.get(reverse("core:service_detail", args=[9999])).status_code == 404


def test_branch_partial(client, site):
    response = client.get(reverse("core:branch_detail", args=[site.branch.pk]))
    assert response.status_code == 200
    assert "Test Branch" in html(response)


def test_coordinate_directions(site):
    branch = Branch.objects.get(name="Test Branch")
    url = _directions_url(branch)
    assert "destination=-19.4550000%2C29.8170000" in url
    assert "travelmode=driving" in url


def test_track_event_records_the_action(client, site):
    response = client.post(
        reverse("core:track_event"),
        {"event_type": "service", "label": site.service.name, "page": "/", "target": "#service", "service_id": site.service.pk},
    )
    assert response.status_code == 200
    event = SiteEvent.objects.get()
    assert event.event_type == "service"
    assert event.service == site.service


def test_track_event_falls_back_to_other_for_unknown_types(client, site):
    client.post(reverse("core:track_event"), {"event_type": "nonsense"})
    assert SiteEvent.objects.get().event_type == "other"


def test_track_event_rejects_get(client, site):
    assert client.get(reverse("core:track_event")).status_code == 405
