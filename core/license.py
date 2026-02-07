import requests
import time
from core.hwid import get_hwid

# LICENSE_SERVER = "https://us-central1-whatsappsenderpro-3911f.cloudfunctions.net/verifyLicense"
LICENSE_SERVER = "http://127.0.0.1:5001/whatsappsenderpro-3911f/us-central1/verifyLicense"


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
            "licenseKey": "LICENSE-001",  # أضف المفتاح الصحيح هنا
            "app": "WhatsAppSenderPro"
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
