import base64
import time
from typing import Tuple

import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from jose import jwt


def _to_jwk(key: rsa.RSAPrivateKey, kid: str = "test") -> Tuple[str, dict]:
    """Return PEM private key and JWKS for the given RSA key."""
    priv_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub = key.public_key().public_numbers()
    n = (
        base64.urlsafe_b64encode(pub.n.to_bytes((pub.n.bit_length() + 7) // 8, "big"))
        .rstrip(b"=")
        .decode()
    )
    e = base64.urlsafe_b64encode(pub.e.to_bytes(3, "big")).rstrip(b"=").decode()
    jwks = {
        "keys": [
            {"kty": "RSA", "use": "sig", "alg": "RS256", "kid": kid, "n": n, "e": e}
        ]
    }
    return priv_pem.decode(), jwks


@pytest.fixture()
def rsa_keys():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return _to_jwk(key)


@pytest.fixture()
def valid_token(rsa_keys):
    priv, _ = rsa_keys
    return jwt.encode(
        {"sub": "user", "aud": "test", "iss": "test-issuer"},
        priv,
        algorithm="RS256",
        headers={"kid": "test"},
    )


@pytest.fixture()
def expired_token(rsa_keys):
    priv, _ = rsa_keys
    return jwt.encode(
        {
            "sub": "user",
            "aud": "test",
            "iss": "test-issuer",
            "exp": int(time.time()) - 10,
        },
        priv,
        algorithm="RS256",
        headers={"kid": "test"},
    )
