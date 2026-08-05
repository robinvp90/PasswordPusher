from __future__ import annotations

import secrets
from typing import Any, Dict, Optional

import httpx

from .settings import PWPUSH_API_BASE_URL, PWPUSH_API_TOKEN


def _api_headers() -> Dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if PWPUSH_API_TOKEN:
        headers["Authorization"] = f"Bearer {PWPUSH_API_TOKEN}"
    return headers


def _pwpush_url(path: str) -> str:
    return f"{PWPUSH_API_BASE_URL.rstrip('/')}{path}"


def create_push(payload: Dict[str, Any]) -> Dict[str, Any]:
    url = _pwpush_url("/p.json")
    with httpx.Client(timeout=30.0) as client:
        response = client.post(url, json={"password": payload}, headers=_api_headers())
        response.raise_for_status()
        return response.json()


def generate_passphrase() -> str:
    return secrets.token_urlsafe(16)
