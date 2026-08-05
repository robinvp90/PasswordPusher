import math
import uuid
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from .auth import auth_callback, get_session_user, login, logout, require_admin_user
from .database import get_db
from .models import Tenant
from .pwpush_client import create_push, generate_passphrase
from .schemas import PushRequest, TenantCreateRequest

router = APIRouter()

@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@router.get("/login")
async def oidc_login(request: Request):
    return await login(request)

@router.get("/logout")
async def oidc_logout(request: Request):
    return await logout(request)

@router.get("/auth/callback")
async def oidc_callback(request: Request):
    return await auth_callback(request)

@router.get("/api/v1/user")
def current_user(request: Request):
    user = get_session_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user

@router.post("/api/v1/tenants")
def create_tenant(payload: TenantCreateRequest, db=Depends(get_db), request: Request = None):
    require_admin_user(request)
    tenant_id = f"tenant-{uuid.uuid4().hex[:8]}"
    tenant = Tenant(
        tenant_id=tenant_id,
        tenant_name=payload.tenant_name,
        contact_email=payload.contact_email,
        reseller_id=payload.reseller_id,
        status="provisioning",
    )
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return {
        "tenant_id": tenant.tenant_id,
        "tenant_name": tenant.tenant_name,
        "contact_email": tenant.contact_email,
        "reseller_id": tenant.reseller_id,
        "status": tenant.status,
    }

@router.get("/api/v1/tenants")
def list_tenants(db=Depends(get_db), request: Request = None):
    require_admin_user(request)
    tenants = db.query(Tenant).all()
    return [
        {
            "tenant_id": tenant.tenant_id,
            "tenant_name": tenant.tenant_name,
            "contact_email": tenant.contact_email,
            "reseller_id": tenant.reseller_id,
            "status": tenant.status,
            "created_at": tenant.created_at.isoformat() if tenant.created_at else None,
            "updated_at": tenant.updated_at.isoformat() if tenant.updated_at else None,
        }
        for tenant in tenants
    ]

@router.patch("/api/v1/tenants/{tenant_id}")
def update_tenant_status(
    tenant_id: str,
    status: str,
    db=Depends(get_db),
    request: Request = None,
):
    require_admin_user(request)
    tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    if tenant is None:
        raise HTTPException(status_code=404, detail="tenant not found")
    if status not in {"provisioning", "active", "suspended", "deprovisioned"}:
        raise HTTPException(status_code=400, detail="invalid tenant status")
    tenant.status = status
    db.commit()
    db.refresh(tenant)
    return {
        "tenant_id": tenant.tenant_id,
        "status": tenant.status,
    }

@router.post("/api/v1/push")
def create_password_push(payload: PushRequest, db=Depends(get_db), request: Request = None):
    require_admin_user(request)
    tenant = db.query(Tenant).filter(Tenant.tenant_id == payload.tenant_id).first()
    if tenant is None:
        raise HTTPException(status_code=404, detail="tenant not found")

    passphrase = generate_passphrase() if payload.require_passphrase else None
    expire_after_days = math.ceil(payload.expires_after_minutes / 1440) if payload.expires_after_minutes else None

    pwpush_payload = {
        "payload": payload.secret_text,
        "expire_after_views": payload.expires_after_views,
    }
    if expire_after_days:
        pwpush_payload["expire_after_days"] = expire_after_days
    if passphrase:
        pwpush_payload["passphrase"] = passphrase

    pwpush_response = create_push(pwpush_payload)

    return {
        "tenant_id": tenant.tenant_id,
        "recipient_email": payload.recipient_email,
        "share_url": pwpush_response.get("html_url"),
        "json_url": pwpush_response.get("json_url"),
        "expires_after_views": payload.expires_after_views,
        "expires_after_minutes": payload.expires_after_minutes,
        "require_passphrase": payload.require_passphrase,
        "passphrase": passphrase,
        "status": "push-created",
    }
