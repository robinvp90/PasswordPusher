# Secure Multi-Tenant Password Pusher Control Plane

This repository is a starter for a secure multi-tenant integration around the open source Password Pusher project.

## What this starter includes

- FastAPI based control plane for hosting a tenant-aware secure sharing workflow
- Entra ID SSO-ready identity integration patterns
- Tenant isolation model for customer data separation
- Docker Compose deployment asset
- Azure deployment skeleton using Bicep

## Architecture goals

- Internal admin authentication via Microsoft Entra ID SSO
- Reseller-style tenant onboarding and management
- Separate tenant namespace and isolated data boundary
- Password Pusher as the secure secret-sharing engine
- Least-privilege access and audit-friendly design

## Recommended production deployment

For regulated or enterprise customer data, prefer a per-tenant deployment model:

- one environment per tenant, or
- one shared environment with strict tenant-aware data isolation

The code in this repo is intentionally scoped to demonstrate the control plane, integration pattern, and deployment assets. Production hardening should add:

- real Entra ID OIDC integration
- tenant-specific encryption keys
- database segregation
- secret scanning and policy enforcement
- SIEM/audit export
- security review for ISO-aligned controls

## Run locally

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker Compose

```bash
docker compose up --build
```

### Full integrated deployment

This repository includes a control plane and a sample Password Pusher deployment path.
Use the full integrated compose manifest at `PasswordPusher/deploy/docker/docker-compose.tenant.yml` if you want both the control plane and Password Pusher engine in one stack.

### Environment variables

Copy `.env.example` to `.env` and populate the required values:

- `PWPUSH_API_TOKEN`
- `SESSION_SECRET_KEY`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_TENANT_ID`
- `OIDC_ALLOWED_DOMAIN`
- `OIDC_REDIRECT_URI`

### Local run

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Azure deployment

Use the Bicep in `infra/main.bicep` as the starting point for Azure Container Apps.

## Security notes

This starter does not replace formal compliance, penetration testing, or platform security review. Use it as an implementation baseline only.
