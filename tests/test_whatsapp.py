from apps.core.models import Package, QuoteRequest
from apps.core.whatsapp import quote_whatsapp_message, whatsapp_link


def test_link_keeps_digits_only():
    assert whatsapp_link("+263 71 234 5678", "Hi").startswith("https://wa.me/263712345678?text=")


def test_link_is_hash_when_number_missing():
    assert whatsapp_link("", "Hi") == "#"


def test_link_encodes_the_message():
    assert "Hello%20there" in whatsapp_link("263712345678", "Hello there")


def test_quote_message_includes_the_details():
    quote = QuoteRequest(
        name="Tendai", phone="0771234567", location="Mvurwi", message="Fridge and lights",
        package=Package(name="3.3 KVA"),
    )
    text = quote_whatsapp_message(quote)
    for expected in ("Name: Tendai", "Phone: 0771234567", "Location: Mvurwi", "Package: 3.3 KVA", "Details: Fridge and lights"):
        assert expected in text


def test_quote_message_skips_empty_parts():
    quote = QuoteRequest(name="Tendai", phone="0771234567", location="Mvurwi")
    text = quote_whatsapp_message(quote)
    assert "Package:" not in text
    assert "Details:" not in text
