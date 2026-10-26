# FieldFlow AI

AI-powered service operations platform for field service companies, plumbing and HVAC teams, maintenance businesses, and commercial service organizations.

Built and owned by: ki9521787@gmail.com

FieldFlow AI helps service businesses manage work orders, dispatch technicians, coordinate jobs, track progress, and report operational performance from a single system.

## Why it matters

Most service businesses lose money not because they lack jobs, but because operations are chaotic:
- work orders arrive from phone, text, email, and WhatsApp
- assignments are manual and inconsistent
- dispatch decisions are slow and poorly tracked
- field teams do not know what is complete
- customers do not know the status of work
- reporting lives in spreadsheets and scattered messages
- productivity is invisible and hard to measure

FieldFlow AI centralizes those workflows into one operational command center.

## Product vision

FieldFlow AI is a SaaS operating system for service teams with:
- work order lifecycle management
- client and site tracking
- technician dispatch and scheduling
- completion visibility
- photo and file attachments
- SLA monitoring
- business analytics
- white-label and multi-client potential
- AI-assisted takeoff and estimation for trades businesses

## Core features

- dashboard with KPI cards
- work order creation and editing
- client and site management
- technician assignment
- search and filtering
- scheduled jobs and priorities
- completion tracking
- export-ready reporting
- role-aware architecture for scalable operations
- AI-powered future dispatch and estimation workflows

## Security-first product posture

This project is designed to evolve toward professional SaaS-grade security:
- role-based access control
- secret handling via environment configuration
- CORS restrictions
- hashing for user credentials
- JWT-ready authentication architecture
- audit logging foundations
- structured validation
- controlled file and upload handling

## Product positioning

FieldFlow AI is built for:
- plumbing and HVAC businesses
- field service companies
- commercial maintenance teams
- contractors and service organizations
- repair and facilities operations
- technical support teams

## Tech stack

- Backend: Python, FastAPI, SQLAlchemy
- Frontend: React, TypeScript, Vite
- Database: SQLite for MVP, PostgreSQL-ready for production
- Deployment: Docker / Docker Compose

## Commercial model

This is designed as a serious SaaS product with recurring revenue potential:
- SaaS subscriptions
- team and enterprise plans
- onboarding and setup services
- white-label deployments
- custom integrations and API access
- premium support

## Start locally

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

## Ownership and attribution

Built and designed by: ki9521787@gmail.com

This repository is intended as a serious SaaS foundation for service operations and can be adapted for commercial use.

## Contact

Email: ki9521787@gmail.com
Website: https://fieldflowai.com
GitHub: https://github.com/ki9521787ki9521787/fieldflow-ai
