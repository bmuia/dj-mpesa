import base64
import requests
from django.conf import settings
from rest_framework.response import Response


def get_access_token():

    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET

    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, headers=headers)
    return response.json().get("access_token")

def simulate_c2b_payment(shortcode=None, amount=0, phone_number="", bill_ref="Test", command="CustomerPayBillOnline"):
    
    shortcode = shortcode or getattr(settings, "MPESA_DEFAULT_SHORTCODE", None)

    if not shortcode:
        return {"error": "Shortcode not provided and MPESA_DEFAULT_SHORTCODE not set in settings"}

    access_token = get_access_token()
    if not access_token:
        return {"error": "Unable to get access token"}

    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "ShortCode": shortcode,
        "CommandID": command,
        "Amount": amount,
        "Msisdn": phone_number,
        "BillRefNumber": bill_ref
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()
