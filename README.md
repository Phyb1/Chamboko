# Chamboko Solar Technology: demo site

A Django site built on the PHYB Signpost template for the **$80 (Basic) package**:
Home, Services, About and Contact pages, an editable packages and prices list, and a quote
request form.

## What the client can manage at `/admin/`

| Section | What it controls |
| --- | --- |
| Site & contact information | Business name, hero and About text, phone, email, WhatsApp number, address, brand colours |
| Packages | Name, price, badge, what is included, what it can power, order, show/hide |
| Services | Name, description, icon, order, show/hide |
| Quote requests | Inbox of requests from the website. Only the status can be changed |
| Branches | Extra locations (a section appears on the Contact page when there is more than one) |

The dashboard shows the last 30 days of clicks and quote requests.

## How quote requests work

1. The visitor fills in the form on `/contact/`.
2. The request is **saved to the database first**, so it is never lost.
3. The business is **emailed** (if `QUOTE_NOTIFY_EMAIL` is set). A mail failure is logged and never shown to the visitor.
4. The thank-you page offers a **WhatsApp button with the details already typed in**. The visitor still has to tap send, because a website cannot send WhatsApp messages by itself.

A hidden honeypot field drops most spam bots.

## Run the tests

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest
```

The suite covers the models, every page, the quote form (valid, invalid, spam, email on and off, email failure), the admin, the demo content, and a check that the models and migrations agree. If `test_models_and_migrations_are_in_sync` fails, run `python manage.py makemigrations core`.

## Run locally

```bash
cp .env.example .env              # then set SECRET_KEY; leave SERVICES_JSON and BRANCHES_JSON out
python manage.py migrate
python manage.py loaddata chamboko_demo
python manage.py createsuperuser
DJANGO_SETTINGS_MODULE=config.settings.dev python manage.py runserver
```

`loaddata chamboko_demo` replaces the default profile with the Chamboko content (profile, six services, the Harare address and two packages). Run it once on a new database; running it again resets those records to the demo values.

## Deploy to a cPanel subdomain

1. Create the subdomain and a Python app for it in cPanel, with the app root pointing at this folder and `passenger_wsgi.py` as the entry point.
2. Upload the project and copy `.env.example` to `.env`. Set at least `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` (with `https://`), and the `STATIC_URL`/`MEDIA_URL` for the subdomain. Production refuses to start with the placeholder `SECRET_KEY`.
3. In the app's virtualenv: `pip install -r requirements.txt`, then
   `python manage.py migrate`, `python manage.py loaddata chamboko_demo`,
   `python manage.py collectstatic --noinput`, `python manage.py createsuperuser`.
4. LiteSpeed bypasses WhiteNoise, so add the usual static-files symlink for the subdomain's base path (the same fix used on the other PHYB sites).
5. For email, create a mailbox in cPanel and set the `EMAIL_*` values and `QUOTE_NOTIFY_EMAIL` in `.env`, then restart the app.

HTMX is loaded from its CDN in `templates/base.html`. To host it yourself, put `htmx.min.js` in `static_src/js/` and point the script tag at it.

## Content to confirm with the client before launch

- **Address:** the old website says *83 Denbigh, Belvedere, Harare*; the flyers say *02 Jacob Cranborn, Harare*.
- **Phone numbers:** the flyers also show 0712 673 691 and +263 775 157 716. The site shows one number.
- **Prices:** the packages use the flyer prices ($1,200 and $2,200). The old website showed different packages and prices.
- **Christmas offer:** the 6.2 KVA package carries a "Christmas special" badge and an extra free panel. Remove both in the admin when the offer ends.
- **Opening hours** and **social media links** are blank.
- **Warranties** are not shown anywhere, because no reliable figures were supplied.
