from unittest.mock import patch

import requests
from django.test import SimpleTestCase

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
