from django import forms
from django.core.exceptions import ValidationError

from .models import Currency


class ConversionForm(forms.Form):
    from_currency = forms.ModelChoiceField(queryset=Currency.objects.filter(is_active=True))
    to_currency = forms.ModelChoiceField(queryset=Currency.objects.filter(is_active=True))
    amount = forms.DecimalField(min_value=0.01, max_digits=18, decimal_places=2)

    def clean(self):
        cleaned_data = super().clean()
        from_currency = cleaned_data.get("from_currency")
        to_currency = cleaned_data.get("to_currency")
        if from_currency and from_currency == to_currency:
            raise ValidationError("From and to currencies must be different.")
        return cleaned_data
