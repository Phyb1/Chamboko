from decimal import Decimal

from django.urls import reverse

from apps.core.models import Package, QuoteRequest


def make_quote(**overrides):
    data = {"name": "Tendai", "phone": "0771234567", "location": "Mvurwi"}
    data.update(overrides)
    return QuoteRequest.objects.create(**data)


def test_dashboard_counts_quote_requests(admin_client, site):
    make_quote()
    make_quote(status=QuoteRequest.Status.CONTACTED)
    response = admin_client.get("/admin/")
    assert response.status_code == 200
    metrics = response.context["signpost_metrics"]
    assert metrics["quotes"] == 2
    assert metrics["new_quotes"] == 1
    assert "Quote requests" in response.content.decode()


def test_quote_inbox_lists_requests(admin_client, site):
    make_quote(name="Inbox Person")
    response = admin_client.get(reverse("signpost_admin:core_quoterequest_changelist"))
    assert response.status_code == 200
    assert "Inbox Person" in response.content.decode()


def test_quote_requests_cannot_be_added_by_hand(admin_client, site):
    assert admin_client.get(reverse("signpost_admin:core_quoterequest_add")).status_code == 403


def test_quote_details_are_read_only_but_status_can_change(admin_client, site):
    quote = make_quote()
    url = reverse("signpost_admin:core_quoterequest_change", args=[quote.pk])
    assert admin_client.get(url).status_code == 200
    response = admin_client.post(url, {"status": "contacted", "name": "Changed Name"})
    assert response.status_code == 302
    quote.refresh_from_db()
    assert quote.status == QuoteRequest.Status.CONTACTED
    assert quote.name == "Tendai"


def test_prices_can_be_edited_in_the_admin(admin_client, site):
    url = reverse("signpost_admin:core_package_change", args=[site.package.pk])
    response = admin_client.post(url, {
        "name": "Test Package", "badge": "", "price": "999.00", "summary": "",
        "includes": "Inverter", "runs": "", "sort_order": 0, "is_active": "on",
    })
    assert response.status_code == 302
    site.package.refresh_from_db()
    assert site.package.price == Decimal("999.00")


def test_package_list_page_loads(admin_client, site):
    assert admin_client.get(reverse("signpost_admin:core_package_changelist")).status_code == 200
