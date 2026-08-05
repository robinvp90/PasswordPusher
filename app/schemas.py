from pydantic import BaseModel

class TenantCreateRequest(BaseModel):
    tenant_name: str
    contact_email: str
    reseller_id: str | None = None

class PushRequest(BaseModel):
    tenant_id: str
    recipient_email: str
    secret_text: str
    expires_after_views: int = 1
    expires_after_minutes: int = 60
    require_passphrase: bool = True
