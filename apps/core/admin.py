from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone

from .models import Branch, Package, QuoteRequest, Service, SiteEvent, SiteProfile


class SignpostAdminSite(admin.AdminSite):
    site_header = "PHYB Signpost"
    site_title = "PHYB Signpost Admin"
    index_title = "Website dashboard"

    def each_context(self, request):
        context = super().each_context(request)
        since = timezone.now() - timedelta(days=30)
        events = SiteEvent.objects.filter(created_at__gte=since)
        context["signpost_metrics"] = {
            "total": events.count(),
            "whatsapp": events.filter(event_type=SiteEvent.EventType.WHATSAPP).count(),
            "directions": events.filter(event_type=SiteEvent.EventType.DIRECTIONS).count(),
            "phone": events.filter(event_type=SiteEvent.EventType.PHONE).count(),
            "email": events.filter(event_type=SiteEvent.EventType.EMAIL).count(),
            "services": events.filter(event_type=SiteEvent.EventType.SERVICE).count(),
            "quotes": QuoteRequest.objects.filter(created_at__gte=since).count(),
            "new_quotes": QuoteRequest.objects.filter(status=QuoteRequest.Status.NEW).count(),
            "top_services": list(
                events.filter(service__isnull=False)
                .values("service__name")
                .annotate(total=Count("id"))
                .order_by("-total")[:5]
            ),
            "top_branches": list(
                events.filter(branch__isnull=False)
                .values("branch__name")
                .annotate(total=Count("id"))
                .order_by("-total")[:5]
            ),
        }
        return context


admin_site = SignpostAdminSite(name="signpost_admin")


@admin.register(SiteProfile, site=admin_site)
class SiteProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Business identity", {"fields": ("site_name", "tagline", "hero_title", "hero_text", "about_title", "about_text", "meta_description")}),
        ("Contact", {"fields": ("phone", "email", "whatsapp_number", "address", "opening_hours", "facebook_url", "instagram_url")}),
        ("Brand", {"fields": ("brand_primary", "brand_dark", "brand_light", "logo_image", "hero_image")}),
    )
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def save_model(self, request, obj, form, change):
        if not change and SiteProfile.objects.exists():
            return
        super().save_model(request, obj, form, change)


@admin.register(Service, site=admin_site)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "sort_order", "is_active", "event_count")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name", "description")
    ordering = ("sort_order", "name")

    @admin.display(description="CTA clicks")
    def event_count(self, obj):
        return obj.events.count()


@admin.register(Package, site=admin_site)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "badge", "sort_order", "is_active")
    list_editable = ("price", "sort_order", "is_active")
    search_fields = ("name", "summary")
    ordering = ("sort_order", "name")
    fieldsets = (
        ("Package", {"fields": ("name", "badge", "price", "summary")}),
        ("Details", {"fields": ("includes", "runs")}),
        ("Display", {"fields": ("sort_order", "is_active")}),
    )


@admin.register(QuoteRequest, site=admin_site)
class QuoteRequestAdmin(admin.ModelAdmin):
    """Inbox for quote requests. Visitors' details are read-only; only the status changes."""
    list_display = ("created_at", "name", "phone", "location", "package", "status")
    list_editable = ("status",)
    list_filter = ("status", "created_at")
    search_fields = ("name", "phone", "email", "location", "message")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_select_related = ("package",)
    readonly_fields = ("name", "phone", "email", "location", "package", "message", "created_at")
    fields = ("status", "name", "phone", "email", "location", "package", "message", "created_at")

    def has_add_permission(self, request):
        return False


@admin.register(Branch, site=admin_site)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "sort_order", "is_active", "directions_count")
    list_editable = ("sort_order", "is_active")
    search_fields = ("name", "address", "phone")
    ordering = ("sort_order", "name")
    fieldsets = (
        ("Branch", {"fields": ("name", "address", "phone", "whatsapp_number")}),
        ("Maps", {"fields": ("google_place_id", "latitude", "longitude")}),
        ("Display", {"fields": ("sort_order", "is_active")}),
    )

    @admin.display(description="Directions clicks")
    def directions_count(self, obj):
        return obj.events.filter(event_type=SiteEvent.EventType.DIRECTIONS).count()


@admin.register(SiteEvent, site=admin_site)
class SiteEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "event_type", "label", "service", "branch", "page")
    list_filter = ("event_type", "created_at")
    search_fields = ("label", "target", "page", "service__name", "branch__name")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    list_select_related = ("service", "branch")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
