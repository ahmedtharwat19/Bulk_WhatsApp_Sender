import base64, os, json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

_SALT = b"WSENDER_V433_SALT"
_PASSWORD = b"WhatsAppSenderPro@2026"

def _get_key():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=_SALT,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(_PASSWORD))

_fernet = Fernet(_get_key())

def encrypt_json(data: dict, path: str):
    raw = json.dumps(data).encode()
    enc = _fernet.encrypt(raw)
    with open(path, "wb") as f:
        f.write(enc)

def decrypt_json(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "rb") as f:
        dec = _fernet.decrypt(f.read())
    return json.loads(dec.decode())
