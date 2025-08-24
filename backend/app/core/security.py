from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import base64
import hmac
import hashlib
import json

from fastapi import HTTPException, status

from .config import settings


def _sign(payload: Dict[str, Any], expires_in_minutes: int) -> str:
    now = datetime.now(tz=timezone.utc)
    payload_copy = dict(payload)
    payload_copy["iat"] = int(now.timestamp())
    payload_copy["exp"] = int((now + timedelta(minutes=expires_in_minutes)).timestamp())
    body = json.dumps(payload_copy, separators=(",", ":")).encode()
    sig = hmac.new(settings.JWT_SECRET.encode(), body, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(body).decode().rstrip("=") + "." + base64.urlsafe_b64encode(sig).decode().rstrip("=")


def _verify(token: str) -> Dict[str, Any]:
    try:
        body_b64, sig_b64 = token.split(".")
        body = base64.urlsafe_b64decode(body_b64 + "==")
        expected_sig = hmac.new(settings.JWT_SECRET.encode(), body, hashlib.sha256).digest()
        sig = base64.urlsafe_b64decode(sig_b64 + "==")
        if not hmac.compare_digest(expected_sig, sig):
            raise ValueError("invalid signature")
        payload = json.loads(body)
        if int(payload.get("exp", 0)) < int(datetime.now(tz=timezone.utc).timestamp()):
            raise ValueError("expired")
        return payload
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


def create_access_token(sub: str, extra: Dict[str, Any] | None = None) -> str:
    payload: Dict[str, Any] = {"sub": sub, "typ": "access"}
    if extra:
        payload.update(extra)
    return _sign(payload, settings.JWT_EXPIRE_MINUTES)


def create_refresh_token(sub: str, extra: Dict[str, Any] | None = None) -> str:
    payload: Dict[str, Any] = {"sub": sub, "typ": "refresh"}
    if extra:
        payload.update(extra)
    return _sign(payload, settings.JWT_REFRESH_EXPIRE_MINUTES)


def verify_token(token: str) -> Dict[str, Any]:
    return _verify(token)
