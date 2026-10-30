from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


class SiteProfile(models.Model):
    """The editable content and contact settings for a Signpost site."""
    site_name = models.CharField(max_length=120, default="Your Business Name")
    tagline = models.CharField(max_length=180, default="Professional services you can trust.")
    hero_title = models.CharField(max_length=220, default="Get the service you need, without the hassle.")
    hero_text = models.TextField(default="Tell customers what you do, where you are and how they can reach you.")
    about_title = models.CharField(max_length=180, default="About Your Business")
    about_text = models.TextField(default="Add a short, clear description of your business here.")
    meta_description = models.CharField(max_length=180, default="Professional services from Your Business Name.")

    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    opening_hours = models.CharField(max_length=180, blank=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    brand_primary = models.CharField(max_length=30, default="#12A8E0")
    brand_dark = models.CharField(max_length=30, default="#071C2C")
    brand_light = models.CharField(max_length=30, default="#F5FBFE")
    logo_image = models.CharField(max_length=255, default="images/brand/logo-placeholder.svg")
    hero_image = models.CharField(max_length=255, default="images/hero-placeholder.svg")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site & contact information"
        verbose_name_plural = "Site & contact information"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteProfile.objects.exists():
            raise ValidationError("Only one Site & contact information record is allowed.")
        super().save(*args, **kwargs)


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=20, default="✦", blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=40, blank=True)
    whatsapp_number = models.CharField(max_length=30, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    google_place_id = models.CharField(max_length=255, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name


def _clean_lines(text):
    """Split a multi-line admin field into tidy items, dropping blanks and bullets."""
    items = []
    for line in (text or "").splitlines():
        item = line.strip().lstrip("•-*· ").strip()
        if item:
            items.append(item)
    return items


class Package(models.Model):
    """A complete solar package with a price the client can edit."""
    name = models.CharField(max_length=120)
    badge = models.CharField(max_length=40, blank=True, help_text="Optional label such as 'Christmas special'.")
    price = models.DecimalField(max_digits=9, decimal_places=2, help_text="Price in US dollars.")
    summary = models.CharField(max_length=200, blank=True)
    includes = models.TextField(blank=True, help_text="What is in the package. One item per line.")
    runs = models.TextField(blank=True, help_text="What the package can power. One item per line.")
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name

    def clean(self):
        if self.price is not None and self.price < 0:
            raise ValidationError({"price": "Price cannot be negative."})

    @property
    def price_display(self):
        """'$1,200' for whole dollars, '$1,199.50' when there are cents."""
        if self.price is None:
            return ""
        price = Decimal(str(self.price))
        if price == price.to_integral_value():
            return f"${price:,.0f}"
        return f"${price:,.2f}"

    def includes_list(self):
        return _clean_lines(self.includes)

    def runs_list(self):
        return _clean_lines(self.runs)


class QuoteRequest(models.Model):
    """A quote request sent through the website form."""

    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        WON = "won", "Won"
        CLOSED = "closed", "Closed"

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=120)
    package = models.ForeignKey(Package, null=True, blank=True, on_delete=models.SET_NULL, related_name="quote_requests")
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} ({self.location})"


class SiteEvent(models.Model):
    class EventType(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        DIRECTIONS = "directions", "Directions"
        PHONE = "phone", "Phone"
        EMAIL = "email", "Email"
        SERVICE = "service", "Service enquiry"
        NAVIGATION = "navigation", "Navigation"
        OTHER = "other", "Other"

    event_type = models.CharField(max_length=30, choices=EventType.choices)
    label = models.CharField(max_length=120, blank=True)
    page = models.CharField(max_length=255, blank=True)
    target = models.CharField(max_length=255, blank=True)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
    branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.SET_NULL, related_name="events")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=("event_type", "created_at"))]

    def __str__(self):
        return f"{self.get_event_type_display()} — {self.label or self.target or self.page}"
