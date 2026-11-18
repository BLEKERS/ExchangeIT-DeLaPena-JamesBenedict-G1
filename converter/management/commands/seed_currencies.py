from django.core.management.base import BaseCommand

from converter.models import Currency

CURRENCIES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "PHP": "Philippine Peso",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "INR": "Indian Rupee",
    "SGD": "Singapore Dollar",
    "NZD": "New Zealand Dollar",
    "HKD": "Hong Kong Dollar",
    "SEK": "Swedish Krona",
    "KRW": "South Korean Won",
    "NOK": "Norwegian Krone",
    "MXN": "Mexican Peso",
    "TWD": "New Taiwan Dollar",
    "ZAR": "South African Rand",
    "BRL": "Brazilian Real",
}


class Command(BaseCommand):
    help = "Seed the supported currencies."

    def handle(self, *args, **options):
        created = 0
        for code, name in CURRENCIES.items():
            currency, was_created = Currency.objects.get_or_create(
                currency_code=code,
                defaults={"currency_name": name, "is_active": True},
            )
            created += was_created
            if not currency.is_active:
                currency.is_active = True
                currency.save(update_fields=["is_active"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Currencies seeded: {created} created, "
                f"{len(CURRENCIES) - created} already existed."
            )
        )
