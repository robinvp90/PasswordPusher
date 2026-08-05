from __future__ import annotations

from typing import Any, Dict, Optional

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import HTTPException, status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from .settings import (
    AZURE_CLIENT_ID,
    AZURE_CLIENT_SECRET,
    AZURE_TENANT_ID,
    OIDC_ALLOWED_DOMAIN,
    OIDC_REDIRECT_URI,
    OIDC_SCOPES,
)

oauth = OAuth()
if AZURE_CLIENT_ID and AZURE_CLIENT_SECRET and AZURE_TENANT_ID:
    oauth.register(
        name="azure",
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET,
        server_metadata_url=(
            f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0/.well-known/openid-configuration"
        ),
        client_kwargs={"scope": OIDC_SCOPES},
    )


async def login(request: Request) -> RedirectResponse:
    if not AZURE_CLIENT_ID or not AZURE_CLIENT_SECRET or not AZURE_TENANT_ID:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Azure OIDC is not configured.",
        )
    return await oauth.azure.authorize_redirect(request, redirect_uri=OIDC_REDIRECT_URI)


async def auth_callback(request: Request) -> RedirectResponse:
    try:
        token = await oauth.azure.authorize_access_token(request)
    except OAuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"OIDC authorization failed: {exc.error}",
        )

    user: Optional[Dict[str, Any]] = None
    try:
        user = await oauth.azure.parse_id_token(request, token)
    except Exception:
        user = None

    if not user:
        user = token.get("userinfo") or {}

    if not user or "email" not in user:
        user = await oauth.azure.userinfo(token=token)

    if not user or "email" not in user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to resolve authenticated user profile.",
        )

    request.session["user"] = {
        "email": user.get("email"),
        "name": user.get("name"),
        "sub": user.get("sub"),
        "preferred_username": user.get("preferred_username"),
        "oid": user.get("oid"),
        "tid": user.get("tid"),
    }
    return RedirectResponse(url="/")


async def logout(request: Request) -> RedirectResponse:
    request.session.pop("user", None)
    return RedirectResponse(url="/")


def get_session_user(request: Request) -> Optional[Dict[str, Any]]:
    return request.session.get("user")


def require_admin_user(request: Request) -> Dict[str, Any]:
    user = get_session_user(request)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required.")

    if OIDC_ALLOWED_DOMAIN:
        email = user.get("email", "")
        if not email.lower().endswith(OIDC_ALLOWED_DOMAIN.lower()):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Authenticated user does not belong to an allowed domain.",
            )

    return user
