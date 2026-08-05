# Tenant control plane starter

This repository now carries a fork-safe baseline for a secure tenant control plane that sits in front of Password Pusher.

## Goal

Support all of the following without coupling your custom business logic into the upstream Password Pusher application:

- Internal admin login via Microsoft Entra ID SSO
- Reseller-style customer tenant onboarding
- Per-customer isolation
- ISO-aligned security defaults
- Docker and Azure deployment paths

## Recommended architecture

1. Use the upstream Password Pusher project as the secret-sharing engine.
2. Add a tenant control plane that manages:
   - tenant metadata
   - reseller ownership
   - customer admins
   - per-tenant policy
   - isolated storage or isolated DB / key scopes
3. Integrate Microsoft Entra ID as the identity provider for internal admins and privileged operations.

## Security baseline

The starter assumes the following enterprise controls:

- Entra ID SSO with MFA required for privileged roles
- RBAC with least privilege
- per-tenant audit logs
- separate tenant access keys or separate database scope per tenant
- TLS everywhere
- secret scanning in the repository
- environment-based configuration and no secrets in source control
- explicit data retention and expiry policy

## Recommended tenant isolation model

For ISO-style customer separation, use one of these patterns:

- Preferred: one isolated Password Pusher instance or DB per tenant
- Alternative: one shared app with tenant-scoped DB rows and separate encryption keys per tenant

The preferred path is stronger and easier to justify for compliance.

## Deployment

- Docker: use `deploy/docker/docker-compose.tenant.yml`
- Azure: use `deploy/azure/container-app.yaml`

## Sync strategy

Keep the upstream Password Pusher repo as `upstream`, and your GitHub fork as `origin`.

Recommended branch strategy:

- `master` or `main`: synced with upstream
- `custom/tenant-control-plane`: your tenant control-plane work

## Notes

This file is a starter design artifact. The production implementation should be completed with your Entra application registration, tenant policy model, and real secret store integration.
