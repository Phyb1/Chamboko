from django import forms

from .models import Package, QuoteRequest

HONEYPOT_FIELD = "hp_website"


class QuoteRequestForm(forms.ModelForm):
    # Honeypot: hidden from real visitors with CSS, so only bots fill it in.
    hp_website = forms.CharField(
        required=False,
        label="Leave this field empty",
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}),
    )

    class Meta:
        model = QuoteRequest
        fields = ("name", "phone", "email", "location", "package", "message")
        labels = {
            "name": "Your name",
            "phone": "Phone or WhatsApp number",
            "email": "Email (optional)",
            "location": "Where are you based?",
            "package": "Package you are interested in",
            "message": "What do you need powered?",
        }
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel", "placeholder": "e.g. 0771234567"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "location": forms.TextInput(attrs={"placeholder": "Suburb or town"}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "For example: fridge, lights, borehole pump"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["package"].queryset = Package.objects.filter(is_active=True)
        self.fields["package"].empty_label = "Not sure yet"

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = [ch for ch in phone if ch.isdigit()]
        if not 9 <= len(digits) <= 15:
            raise forms.ValidationError("Enter a valid phone number, for example 0771234567.")
        return phone

    @property
    def is_spam(self):
        """True when the hidden honeypot field was filled in."""
        return bool(self.cleaned_data.get(HONEYPOT_FIELD))
