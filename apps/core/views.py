import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from .forms import QuoteRequestForm
from .models import Branch, QuoteRequest, Service, SiteEvent
from .site_data import _directions_url, profile_value
from .whatsapp import quote_whatsapp_message, whatsapp_link

logger = logging.getLogger(__name__)

# The visitor's most recent quote is remembered in their session so the thank-you
# page can show it without exposing other people's requests.
QUOTE_SESSION_KEY = "last_quote_id"


def _business_whatsapp(message):
    """WhatsApp link using the number managed in the admin (falls back to .env)."""
    return whatsapp_link(number=profile_value("whatsapp_number") or None, message=message)


class HomeView(TemplateView):
    template_name = "core/home.html"


class ServicesView(TemplateView):
    template_name = "core/services.html"


class AboutView(TemplateView):
    template_name = "core/about.html"


def _notify_quote(quote):
    """Email the business about a new quote request.

    The request is already saved, so a mail failure is logged but never shown to the
    visitor, and the request stays in the admin inbox either way.
    """
    recipient = settings.QUOTE_NOTIFY_EMAIL
    if not recipient:
        return
    lines = [
        f"Name: {quote.name}",
        f"Phone: {quote.phone}",
        f"Email: {quote.email or '-'}",
        f"Location: {quote.location}",
        f"Package: {quote.package.name if quote.package else 'Not sure yet'}",
        "",
        quote.message or "(no details given)",
    ]
    message = EmailMessage(
        subject=f"New quote request from {quote.name}",
        body="\n".join(lines),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
        reply_to=[quote.email] if quote.email else None,
    )
    try:
        message.send()
    except Exception:
        logger.exception("Could not send the notification email for quote request %s", quote.pk)


def contact(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            if form.is_spam:
                return redirect("core:contact")
            quote = form.save()
            _notify_quote(quote)
            request.session[QUOTE_SESSION_KEY] = quote.pk
            return redirect("core:quote_thanks")
    else:
        initial = {}
        package_id = request.GET.get("package", "")
        if package_id.isdigit():
            initial["package"] = int(package_id)
        form = QuoteRequestForm(initial=initial)
    return render(request, "core/contact.html", {"form": form})


def quote_thanks(request):
    quote_id = request.session.get(QUOTE_SESSION_KEY)
    quote = QuoteRequest.objects.select_related("package").filter(pk=quote_id).first() if quote_id else None
    if quote is None:
        return redirect("core:contact")
    return render(request, "core/quote_thanks.html", {
        "quote": quote,
        "quote_whatsapp": _business_whatsapp(quote_whatsapp_message(quote)),
    })


def track_event(request):
    if request.method != "POST":
        return JsonResponse({"ok": False}, status=405)

    event_type = request.POST.get("event_type", "other")[:30]
    allowed = {choice[0] for choice in SiteEvent.EventType}
    if event_type not in allowed:
        event_type = "other"

    service = Service.objects.filter(pk=request.POST.get("service_id")).first() if request.POST.get("service_id") else None
    branch = Branch.objects.filter(pk=request.POST.get("branch_id")).first() if request.POST.get("branch_id") else None

    SiteEvent.objects.create(
        event_type=event_type,
        label=request.POST.get("label", "")[:120],
        page=request.POST.get("page", "")[:255],
        target=request.POST.get("target", "")[:255],
        service=service,
        branch=branch,
    )
    return JsonResponse({"ok": True})


def service_detail(request, pk):
    service = Service.objects.filter(pk=pk, is_active=True).first()
    if not service:
        return HttpResponse("", status=404)
    return HttpResponse(
        render_to_string("partials/service_detail.html", {
            "service": service,
            "service_whatsapp": _business_whatsapp(f"Hi, I'd like to enquire about {service.name}."),
        }, request=request)
    )


def branch_detail(request, pk):
    branch = Branch.objects.filter(pk=pk, is_active=True).first()
    if not branch:
        return HttpResponse("", status=404)
    return HttpResponse(
        render_to_string("partials/branch_detail.html", {
            "branch": branch,
            "directions_url": _directions_url(branch),
        }, request=request)
    )
