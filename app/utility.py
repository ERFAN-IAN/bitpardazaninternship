import os
import random
import requests

kavenegar_token = os.environ.get('KAVENEGARTOKEN')


def send_sms(phone_number, code):
    url = f"https://api.kavenegar.com/v1/{kavenegar_token}/sms/send.json"
    params = {
        "receptor": str(phone_number),
        "message": f"Your password reset code is: {code}"
    }
    try:
        response = requests.post(url, data=params)
        response.raise_for_status()  # Optional: raise exception on failure
        return response.json()
        # print('func')
        # print(code)
        # print(response)
        # print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"[SMS ERROR] Failed to send: {e}")



def otp_code_generator():
    code = random.randint(100000, 999999)

    return code
