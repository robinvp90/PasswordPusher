from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, DateTime, String
from .database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id = Column(String(64), primary_key=True, index=True)
    tenant_name = Column(String(200), nullable=False)
    contact_email = Column(String(200), nullable=False)
    reseller_id = Column(String(100), nullable=True)
    status = Column(String(50), nullable=False, default="provisioning")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
