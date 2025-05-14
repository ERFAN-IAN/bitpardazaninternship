import os
import requests

kavenegar_token = os.environ.get('KAVENEGARTOKEN')


class KavenegarGateway:
    @staticmethod
    def send_sms(device, token, **kwargs):
        phone_number = device.number
        url = f"https://api.kavenegar.com/v1/{kavenegar_token}/sms/send.json"
        params = {
            "receptor": str(phone_number),
            "message": f"Your Code: {token}"
        }
        try:
            response = requests.post(url, data=params)

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"[SMS ERROR] Failed to send: {e}")
