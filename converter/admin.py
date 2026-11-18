from django.contrib import admin

from .models import ConversionHistory, Currency, ExchangeRate, FavoritePair


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("currency_code", "currency_name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("currency_code", "currency_name")


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("from_currency", "to_currency", "rate", "retrieved_at", "source")


@admin.register(FavoritePair)
class FavoritePairAdmin(admin.ModelAdmin):
    list_display = ("user", "from_currency", "to_currency", "created_at")


@admin.register(ConversionHistory)
class ConversionHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "from_currency", "to_currency", "amount", "exchange_rate", "converted_amount", "converted_at")
