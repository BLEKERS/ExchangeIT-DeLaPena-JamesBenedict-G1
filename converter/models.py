from django.conf import settings
from django.db import models


class Currency(models.Model):
    # BR-04: unique 3-char code; BR-05: human-readable name
    currency_code = models.CharField(max_length=3, unique=True)
    currency_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.currency_code} - {self.currency_name}"

    class Meta:
        ordering = ["currency_code"]


class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='rates_to')
    rate = models.DecimalField(max_digits=18, decimal_places=8)  # BR-09
    retrieved_at = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=100)

    class Meta:
        ordering = ["-retrieved_at"]
        constraints = [
            models.CheckConstraint(  # BR-08
                condition=~models.Q(from_currency=models.F('to_currency')),
                name='prevent_same_currency_rate',
            ),
            models.CheckConstraint(  # BR-09
                condition=models.Q(rate__gt=0),
                name='rate_must_be_positive',
            ),
        ]


class FavoritePair(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='fav_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='fav_to')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(  # BR-14
                fields=['user', 'from_currency', 'to_currency'],
                name='unique_user_favorite_pair',
            ),
            models.CheckConstraint(  # BR-15
                condition=~models.Q(from_currency=models.F('to_currency')),
                name='prevent_same_currency_favorite',
            ),
        ]


class ConversionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='conv_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='conv_to')
    amount = models.DecimalField(max_digits=18, decimal_places=2)  # BR-11
    exchange_rate = models.DecimalField(max_digits=18, decimal_places=8)  # BR-18
    converted_amount = models.DecimalField(max_digits=18, decimal_places=2)  # BR-12
    converted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-converted_at"]
        constraints = [
            models.CheckConstraint(  # BR-15
                condition=~models.Q(from_currency=models.F('to_currency')),
                name='prevent_same_currency_conversion',
            ),
            models.CheckConstraint(  # BR-11
                condition=models.Q(amount__gt=0),
                name='amount_must_be_positive',
            ),
            models.CheckConstraint(  # BR-12
                condition=models.Q(converted_amount__gt=0),
                name='converted_amount_must_be_positive',
            ),
        ]
