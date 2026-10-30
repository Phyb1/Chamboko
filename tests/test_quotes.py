from django.core.mail import EmailMessage
from django.urls import reverse

from apps.core.models import QuoteRequest

CONTACT = "core:contact"
THANKS = "core:quote_thanks"


def payload(**overrides):
    data = {
        "name": "Tendai Moyo",
        "phone": "0771234567",
        "email": "",
        "location": "Mvurwi",
        "package": "",
        "message": "Fridge and lights",
    }
    data.update(overrides)
    return data


def html(response):
    return response.content.decode()


def test_valid_request_is_saved_and_redirects(client, site):
    response = client.post(reverse(CONTACT), payload(package=site.package.pk))
    assert response.status_code == 302
    assert response.url == reverse(THANKS)
    quote = QuoteRequest.objects.get()
    assert quote.name == "Tendai Moyo"
    assert quote.package == site.package
    assert quote.status == QuoteRequest.Status.NEW


def test_package_is_optional(client, site):
    client.post(reverse(CONTACT), payload())
    assert QuoteRequest.objects.get().package is None


def test_thanks_page_offers_a_prefilled_whatsapp_message(client, site):
    client.post(reverse(CONTACT), payload(package=site.package.pk))
    response = client.get(reverse(THANKS))
    assert response.status_code == 200
    page = html(response)
    assert "Tendai Moyo" in page
    assert "wa.me/263712345678" in page
    assert "Tendai%20Moyo" in page
    assert "Test%20Package" in page


def test_thanks_page_needs_a_request_in_the_session(client, site):
    response = client.get(reverse(THANKS))
    assert response.status_code == 302
    assert response.url == reverse(CONTACT)


def test_thanks_page_never_shows_someone_elses_request(client, site):
    other = QuoteRequest.objects.create(name="Someone Else", phone="0779999999", location="Harare")
    response = client.get(reverse(THANKS))
    assert response.status_code == 302
    assert other.name not in html(client.get(reverse(CONTACT)))


def test_team_is_emailed_with_a_reply_to(client, site, settings, mailoutbox):
    settings.QUOTE_NOTIFY_EMAIL = "sales@example.com"
    settings.DEFAULT_FROM_EMAIL = "site@example.com"
    client.post(reverse(CONTACT), payload(email="tendai@example.com"))
    assert len(mailoutbox) == 1
    mail = mailoutbox[0]
    assert mail.to == ["sales@example.com"]
    assert mail.from_email == "site@example.com"
    assert mail.reply_to == ["tendai@example.com"]
    assert "Tendai Moyo" in mail.subject
    assert "0771234567" in mail.body
    assert "Mvurwi" in mail.body


def test_no_email_is_sent_when_no_recipient_is_set(client, site, settings, mailoutbox):
    settings.QUOTE_NOTIFY_EMAIL = ""
    client.post(reverse(CONTACT), payload())
    assert mailoutbox == []
    assert QuoteRequest.objects.count() == 1


def test_email_failure_does_not_lose_the_request(client, site, settings, monkeypatch, caplog):
    settings.QUOTE_NOTIFY_EMAIL = "sales@example.com"

    def broken_send(self, *args, **kwargs):
        raise OSError("SMTP server is down")

    monkeypatch.setattr(EmailMessage, "send", broken_send)
    response = client.post(reverse(CONTACT), payload())
    assert response.status_code == 302
    assert response.url == reverse(THANKS)
    assert QuoteRequest.objects.count() == 1
    assert "Could not send the notification email" in caplog.text


def test_name_is_required(client, site):
    response = client.post(reverse(CONTACT), payload(name=""))
    assert response.status_code == 200
    assert "This field is required." in html(response)
    assert QuoteRequest.objects.count() == 0


def test_location_is_required(client, site):
    response = client.post(reverse(CONTACT), payload(location=""))
    assert response.status_code == 200
    assert QuoteRequest.objects.count() == 0


def test_short_phone_numbers_are_rejected(client, site):
    response = client.post(reverse(CONTACT), payload(phone="123"))
    assert response.status_code == 200
    assert "Enter a valid phone number" in html(response)
    assert QuoteRequest.objects.count() == 0


def test_phone_numbers_with_spaces_and_plus_are_accepted(client, site):
    response = client.post(reverse(CONTACT), payload(phone="+263 77 123 4567"))
    assert response.status_code == 302
    assert QuoteRequest.objects.get().phone == "+263 77 123 4567"


def test_bad_email_is_rejected(client, site):
    response = client.post(reverse(CONTACT), payload(email="not-an-email"))
    assert response.status_code == 200
    assert QuoteRequest.objects.count() == 0


def test_inactive_packages_cannot_be_chosen(client, site):
    site.package.is_active = False
    site.package.save()
    response = client.post(reverse(CONTACT), payload(package=site.package.pk))
    assert response.status_code == 200
    assert QuoteRequest.objects.count() == 0


def test_invalid_form_keeps_what_the_visitor_typed(client, site):
    page = html(client.post(reverse(CONTACT), payload(phone="123", name="Tendai Moyo")))
    assert 'value="Tendai Moyo"' in page


def test_honeypot_requests_are_dropped(client, site, settings, mailoutbox):
    settings.QUOTE_NOTIFY_EMAIL = "sales@example.com"
    response = client.post(reverse(CONTACT), payload(hp_website="http://spam.example"))
    assert response.status_code == 302
    assert response.url == reverse(CONTACT)
    assert QuoteRequest.objects.count() == 0
    assert mailoutbox == []


def test_package_is_preselected_from_the_query_string(client, site):
    page = html(client.get(reverse(CONTACT), {"package": site.package.pk}))
    assert f'value="{site.package.pk}" selected' in page


def test_a_non_numeric_package_in_the_query_string_is_ignored(client, site):
    assert client.get(reverse(CONTACT), {"package": "abc"}).status_code == 200
