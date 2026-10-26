# Security Policy

## Reporting a Vulnerability

If you discover a security issue in FieldFlow AI, please report it privately to:

- Email: ki9521787@gmail.com

Please do not open a public GitHub issue for security problems until the issue has been reviewed and a coordinated fix is available.

## Security principles

This project is designed to evolve toward secure production use with:
- role-based access control,
- hashed passwords,
- environment-based secrets,
- strict CORS configuration,
- JWT-ready authentication flow,
- audit and activity logging,
- tenant isolation for multi-client deployments,
- input validation and sanitization,
- secure file upload controls.

## Supported environments

This project is currently a strong MVP foundation. It is not yet a full production-grade multi-tenant SaaS deployment and should be treated as such until hardened for production use.

## Recommended hardening before production usage

- use PostgreSQL instead of SQLite,
- run behind HTTPS with a reverse proxy,
- enable secure session / token handling,
- rotate secrets regularly,
- store secrets in a managed secret store,
- enforce strict role permissions,
- enable audit logs and monitoring,
- isolate uploads and service data,
- validate file types and enforce upload size limits.

## Ownership and responsibility

This project is built and owned by ki9521787@gmail.com.
