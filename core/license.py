import requests
import time
from core.hwid import get_hwid

LICENSE_SERVER = "https://your-license-server.com/verify"

class LicenseError(Exception):
    pass

class LicenseManager:
    def __init__(self):
        self.hwid = get_hwid()

    def verify(self):
        if not self.hwid:
            raise LicenseError("HWID_ERROR")

        payload = {
            "hwid": self.hwid,
            "app": "WhatsAppSenderPro",
            "version": "4.3.3"
        }

        try:
            r = requests.post(LICENSE_SERVER, json=payload, timeout=10)
            if r.status_code != 200:
                raise LicenseError("SERVER_ERROR")

            data = r.json()

            if not data.get("valid"):
                raise LicenseError("LICENSE_INVALID")

            if data.get("expired"):
                raise LicenseError("LICENSE_EXPIRED")

            return data  # contains expiry, plan, etc.

        except requests.exceptions.RequestException:
            raise LicenseError("NO_INTERNET")
