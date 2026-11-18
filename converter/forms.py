from django import forms
from django.core.exceptions import ValidationError

from .models import Currency


class ConversionForm(forms.Form):
    from_currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "input-dark"}),
    )
    to_currency = forms.ModelChoiceField(
        queryset=Currency.objects.filter(is_active=True),
        widget=forms.Select(attrs={"class": "input-dark"}),
    )
    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=18,
        decimal_places=2,
        widget=forms.NumberInput(attrs={"class": "input-dark", "min": "0.01"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        from_currency = cleaned_data.get("from_currency")
        to_currency = cleaned_data.get("to_currency")
        if from_currency and from_currency == to_currency:
            raise ValidationError("From and to currencies must be different.")
        return cleaned_data
