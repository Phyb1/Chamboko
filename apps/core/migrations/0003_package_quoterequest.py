import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_rename_core_siteev_event_ti_8c3f0a_idx_core_siteev_event_t_46b6f9_idx"),
    ]

    operations = [
        migrations.CreateModel(
            name="Package",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("badge", models.CharField(blank=True, help_text="Optional label such as 'Christmas special'.", max_length=40)),
                ("price", models.DecimalField(decimal_places=2, help_text="Price in US dollars.", max_digits=9)),
                ("summary", models.CharField(blank=True, max_length=200)),
                ("includes", models.TextField(blank=True, help_text="What is in the package. One item per line.")),
                ("runs", models.TextField(blank=True, help_text="What the package can power. One item per line.")),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ("sort_order", "name")},
        ),
        migrations.CreateModel(
            name="QuoteRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=40)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("location", models.CharField(max_length=120)),
                ("message", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("new", "New"), ("contacted", "Contacted"), ("won", "Won"), ("closed", "Closed")], default="new", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("package", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="quote_requests", to="core.package")),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]
