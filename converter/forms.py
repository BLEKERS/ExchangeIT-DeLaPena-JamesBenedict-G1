from django import forms
from django.core.exceptions import ValidationError

from .models import Currency, FavoritePair


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


class FavoritePairForm(forms.ModelForm):
    class Meta:
        model = FavoritePair
        fields = ["from_currency", "to_currency"]
        widgets = {
            "from_currency": forms.Select(attrs={"class": "input-dark"}),
            "to_currency": forms.Select(attrs={"class": "input-dark"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        cleaned_data = super().clean()
        from_currency = cleaned_data.get("from_currency")
        to_currency = cleaned_data.get("to_currency")
        if from_currency and to_currency:
            if from_currency == to_currency:
                raise ValidationError("From and to currencies must be different.")
            if self.user:
                duplicate = FavoritePair.objects.filter(
                    user=self.user,
                    from_currency=from_currency,
                    to_currency=to_currency,
                )
                if self.instance.pk:
                    duplicate = duplicate.exclude(pk=self.instance.pk)
                if duplicate.exists():
                    raise ValidationError("This favorite pair already exists.")
        return cleaned_data
