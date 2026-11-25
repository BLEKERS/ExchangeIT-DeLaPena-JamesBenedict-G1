from decimal import Decimal
from unittest.mock import patch

import requests
from django.db import IntegrityError, transaction
from django.test import Client, SimpleTestCase, TestCase

from accounts.models import User
from converter.models import ConversionHistory, Currency, FavoritePair
from converter.services import get_exchange_rate


class GetExchangeRateTests(SimpleTestCase):
    @patch("converter.services.requests.get")
    def test_returns_rate(self, mock_get):
        mock_get.return_value.json.return_value = {"rates": {"EUR": 0.92}}

        self.assertEqual(
            get_exchange_rate("USD", "EUR"),
            {"rate": 0.92, "source": "Frankfurter"},
        )

    @patch("converter.services.requests.get")
    def test_returns_none_when_api_fails(self, mock_get):
        mock_get.side_effect = requests.RequestException

        self.assertIsNone(get_exchange_rate("USD", "TWD"))


class CoreFeatureTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usd = Currency.objects.create(currency_code="USD", currency_name="US Dollar")
        self.eur = Currency.objects.create(currency_code="EUR", currency_name="Euro")
        self.user_a = User.objects.create_user(
            email="user-a@example.com", password="testpass123", full_name="User A"
        )
        self.user_b = User.objects.create_user(
            email="user-b@example.com", password="testpass123", full_name="User B"
        )

    def conversion_post(self):
        return {
            "amount": "100.00",
            "from_currency": self.usd.pk,
            "to_currency": self.eur.pk,
        }

    def test_convert_view_requires_login(self):
        response = self.client.get("/converter/convert/")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/login/"))

    def test_valid_conversion(self):
        self.client.force_login(self.user_a)
        with patch("converter.services.requests.get") as mock_get:
            mock_get.return_value.json.return_value = {"rates": {"EUR": 0.92}}
            response = self.client.post(
                "/converter/convert/", self.conversion_post(), follow=True
            )

        self.assertEqual(response.status_code, 200)
        record = ConversionHistory.objects.get(user=self.user_a)
        self.assertEqual(record.amount, Decimal("100.00"))
        self.assertEqual(record.converted_amount, Decimal("92.00"))
        self.assertContains(response, "Successfully converted")

    def test_invalid_conversion_same_currency(self):
        self.client.force_login(self.user_a)
        with patch("converter.services.requests.get") as mock_get:
            response = self.client.post(
                "/converter/convert/",
                {**self.conversion_post(), "to_currency": self.usd.pk},
            )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "From and to currencies must be different.")
        self.assertFalse(ConversionHistory.objects.exists())
        mock_get.assert_not_called()

    def test_api_failure_handling(self):
        self.client.force_login(self.user_a)
        with patch("converter.services.requests.get") as mock_get:
            mock_get.return_value.status_code = 404
            mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("404")
            response = self.client.post(
                "/converter/convert/", self.conversion_post(), follow=True
            )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(ConversionHistory.objects.exists())
        self.assertContains(
            response, "This currency pair is not supported by our rate provider."
        )

    def test_user_cannot_delete_others_history(self):
        record = ConversionHistory.objects.create(
            user=self.user_a,
            from_currency=self.usd,
            to_currency=self.eur,
            amount=Decimal("100.00"),
            exchange_rate=Decimal("0.92000000"),
            converted_amount=Decimal("92.00"),
        )
        self.client.force_login(self.user_b)

        response = self.client.post(f"/converter/history/delete/{record.pk}/")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(ConversionHistory.objects.filter(pk=record.pk).exists())

    def test_user_cannot_delete_others_favorite(self):
        favorite = FavoritePair.objects.create(
            user=self.user_a, from_currency=self.usd, to_currency=self.eur
        )
        self.client.force_login(self.user_b)

        response = self.client.post(f"/converter/favorites/delete/{favorite.pk}/")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(FavoritePair.objects.filter(pk=favorite.pk).exists())

    def test_model_constraint_prevent_negative_amount(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            ConversionHistory.objects.create(
                user=self.user_a,
                from_currency=self.usd,
                to_currency=self.eur,
                amount=Decimal("-1.00"),
                exchange_rate=Decimal("0.92000000"),
                converted_amount=Decimal("92.00"),
            )

    def test_admin_required_blocks_regular_user(self):
        self.client.force_login(self.user_a)

        response = self.client.get("/dashboard/admin/")

        self.assertIn(response.status_code, (302, 403))
