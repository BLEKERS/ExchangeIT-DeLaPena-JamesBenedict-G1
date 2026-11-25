import requests

FRANKFURTER_URL = "https://api.frankfurter.app/latest"


def get_exchange_rate(from_code: str, to_code: str) -> dict | None:
    response = None
    try:
        response = requests.get(
            FRANKFURTER_URL,
            params={"from": from_code, "to": to_code},
            timeout=10,
        )
        response.raise_for_status()
        rates = response.json()["rates"]
        if to_code not in rates:
            return {"error": "unsupported_currency"}
        return {"rate": float(rates[to_code]), "source": "Frankfurter"}
    except requests.HTTPError:
        if response is not None and response.status_code == 404:
            return {"error": "unsupported_currency"}
        return None
    except (ValueError, KeyError, TypeError):
        return {"error": "unsupported_currency"}
    except requests.RequestException:
        return None
