import hmac
import hashlib
import os

KEY = (os.getenv('FORENSICS_SIGN_KEY') or 'dev-sign-key').encode()

def sign_message(message: bytes) -> str:
    mac = hmac.new(KEY, message, hashlib.sha256).hexdigest()
    return mac

