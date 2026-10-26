# FieldFlow AI

AI-powered service work order SaaS platform for field service companies.

Built and owned by ki9521787@gmail.com.

FieldFlow AI is a premium service operations platform built for field service companies, maintenance teams, repair businesses, contractors, and service organizations that need real operational control across jobs, teams, sites, and customer communication.

This repository contains a serious MVP foundation for a real SaaS business.

## Why this product matters

Most service companies lose money not because they lack clients, but because operations are chaotic:
- work orders arrive by phone, text, email, and WhatsApp,
- tasks are assigned manually and inconsistently,
- dispatch decisions are slow and poorly tracked,
- field teams do not know what is complete,
- customers do not know the status of the work,
- reporting lives in scattered spreadsheets and messages,
- productivity is hidden and cannot be measured.

FieldFlow AI centralizes workflows into one operational command center.

## Product vision

This is not another simple task board.

FieldFlow AI is an operational system for service businesses with:
- work order lifecycle management,
- client and site tracking,
- technician dispatch and scheduling,
- progress visibility,
- file and photo attachments,
- SLA monitoring,
- business analytics,
- white-label SaaS potential,
- AI dispatching for future product expansion.

## Core features

- dashboard with KPI cards,
- order creation and editing,
- client and site management,
- technician assignment,
- search and filtering,
- scheduled jobs and priorities,
- completion tracking,
- file and photo attachment support,
- export-ready reporting,
- role-ready architecture for future scaling,
- future AI-powered dispatch assistant.

## Security-first product posture

This product is designed to evolve toward professional SaaS-grade security:
- role-based access control,
- secure secret handling,
- CORS restrictions,
- secure password hashing,
- JWT-ready authentication flow,
- audit logging,
- tenant isolation,
- structured data validation,
- safe file handling and uploads.

## Product positioning

FieldFlow AI is built for:
- service companies,
- field teams,
- maintenance and repair businesses,
- HVAC and plumbing firms,
- cleaning and janitorial organizations,
- property service operations,
- technical support teams,
- facilities and maintenance companies.

## Tech stack

- Backend: Python, FastAPI, SQLAlchemy
- Frontend: React, TypeScript, Vite
- Styling: custom SaaS dashboard styling
- Database: SQLite for local MVP, PostgreSQL-ready for production
- Deployment: Docker / Docker Compose
- Security model: secure secrets, CORS, password hashing, auth-ready architecture

## Commercial model

This is designed as a real SaaS product with strong recurring revenue:
- monthly SaaS subscriptions,
- team and enterprise tiers,
- onboarding and setup fees,
- custom integrations,
- white-label deployments,
- API access,
- premium support plans.

## Fast start

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host
```

Open in browser:

```text
http://localhost:5173
```

### Docker

```bash
docker-compose up --build
```

## Demo credentials

Username: admin
Password: admin123

## Project structure

- backend/
  - app/
  - requirements.txt
- frontend/
  - src/
- docker-compose.yml
- README.md
- SECURITY.md
- LICENSE

## Roadmap

### MVP
- work orders
- clients and sites
- dashboards and metrics
- quick creation flows
- role-ready auth foundation
- export-friendly reporting

### Next phase
- AI dispatch assistant
- client portal
- SLA tracking and alerts
- calendar sync
- map-based routing
- file storage and attachments
- white-label deployments

### Enterprise phase
- RBAC and access scoping
- tenant isolation
- audit trails
- secure file handling
- custom integrations
- API platform
- billing and subscriptions

## Contact

Email: ki9521787@gmail.com
Website: https://fieldflowai.com
GitHub: https://github.com/ki9521787ki9521787/fieldflow-ai

## Copyright and attribution

Built and designed by ki9521787@gmail.com.

This project is intended to be a serious SaaS starter for service businesses and can be adapted into a commercial product.
