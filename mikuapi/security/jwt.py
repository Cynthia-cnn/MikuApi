

import base64
import json
import time
import hmac
import hashlib

from mikuapi.config import settings


SECRET_KEY = settings.SECRET_KEY


def _b64_encode(data):
    return base64.urlsafe_b64encode(
        json.dumps(data).encode()
    ).decode().rstrip("=")


def _b64_decode(data):
    padding = "=" * (-len(data) % 4)
    return json.loads(
        base64.urlsafe_b64decode(data + padding)
    )


def encode(payload, exp=3600):
    payload = payload.copy()
    payload["exp"] = int(time.time()) + exp

    header = {"alg": "HS256", "typ": "JWT"}

    h = _b64_encode(header)
    p = _b64_encode(payload)

    sig = hmac.new(
        SECRET_KEY.encode(),
        f"{h}.{p}".encode(),
        hashlib.sha256
    ).digest()

    s = base64.urlsafe_b64encode(sig).decode().rstrip("=")

    return f"{h}.{p}.{s}"


def decode(token):
    try:
        h, p, s = token.split(".")

        expected = hmac.new(
            SECRET_KEY.encode(),
            f"{h}.{p}".encode(),
            hashlib.sha256
        ).digest()

        expected_s = base64.urlsafe_b64encode(expected).decode().rstrip("=")

        if s != expected_s:
            return None

        payload = _b64_decode(p)

        if payload.get("exp") < time.time():
            return None

        return payload

    except Exception:
        return None