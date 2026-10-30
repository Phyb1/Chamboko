from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.core.models import Package, QuoteRequest, SiteProfile


def test_price_display_whole_dollars():
    assert Package(name="A", price=Decimal("1200.00")).price_display == "$1,200"


def test_price_display_keeps_cents():
    assert Package(name="A", price=Decimal("1199.50")).price_display == "$1,199.50"


def test_price_display_accepts_plain_numbers():
    assert Package(name="A", price=2200).price_display == "$2,200"


def test_item_lists_drop_blank_lines_and_bullets():
    package = Package(name="A", price=Decimal("1"), includes="• Inverter\n\n- Battery\n  \n* Panels", runs="")
    assert package.includes_list() == ["Inverter", "Battery", "Panels"]
    assert package.runs_list() == []


def test_negative_price_is_rejected():
    with pytest.raises(ValidationError):
        Package(name="A", price=Decimal("-1")).clean()


def test_only_one_site_profile_is_allowed(site):
    with pytest.raises(ValidationError):
        SiteProfile(site_name="Second").save()


def test_quote_request_defaults(db):
    quote = QuoteRequest.objects.create(name="Tendai", phone="0771234567", location="Mvurwi")
    assert quote.status == QuoteRequest.Status.NEW
    assert quote.package is None
    assert str(quote) == "Tendai (Mvurwi)"
