# mikuapi/security/auth.py

from mikuapi.errors import ValidationError
from mikuapi.security.jwt import decode


def require_user(request):
    headers = request.headers()
    auth = headers.get("authorization")

    if not auth or not auth.startswith("Bearer "):
        raise ValidationError("Unauthorized")

    token = auth.split(" ")[1]
    payload = decode(token)

    if not payload:
        raise ValidationError("Invalid token")

    return payload