from urllib.parse import quote
from django.conf import settings


def whatsapp_link(number=None, message="Hi, I'd like to enquire about your services."):
    raw = number if number is not None else settings.WHATSAPP_ORDER_NUMBER
    digits = "".join(ch for ch in str(raw) if ch.isdigit())
    if not digits:
        return "#"
    return f"https://wa.me/{digits}?text={quote(message)}"


def quote_whatsapp_message(quote_request):
    """The WhatsApp text a visitor can send after submitting the quote form."""
    lines = [
        "Hi, I've just requested a quote on your website.",
        f"Name: {quote_request.name}",
        f"Phone: {quote_request.phone}",
        f"Location: {quote_request.location}",
    ]
    if quote_request.package:
        lines.append(f"Package: {quote_request.package.name}")
    if quote_request.message:
        lines.append(f"Details: {quote_request.message}")
    return "\n".join(lines)
