import subprocess
import hashlib

def get_hwid():
    try:
        result = subprocess.check_output(
            "wmic csproduct get uuid", shell=True
        ).decode().split("\n")[1].strip()
        return hashlib.sha256(result.encode()).hexdigest()
    except:
        return None
