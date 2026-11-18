import requests

FRANKFURTER_URL = "https://api.frankfurter.app/latest"


def get_exchange_rate(from_code: str, to_code: str) -> dict | None:
    try:
        response = requests.get(
            FRANKFURTER_URL,
            params={"from": from_code, "to": to_code},
            timeout=10,
        )
        response.raise_for_status()
        return {"rate": float(response.json()["rates"][to_code]), "source": "Frankfurter"}
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None
