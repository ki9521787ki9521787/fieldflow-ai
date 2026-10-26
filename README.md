# fieldflow-ai

AI-powered service work order SaaS platform for field service companies.

## Overview

FieldFlow AI is a modern SaaS platform for service businesses that manage field work, maintenance jobs, repairs, inspections, and technician teams.

It helps teams go from operational chaos to a measurable, trackable workflow:
- create and assign work orders,
- track status and SLAs,
- attach photos and files,
- schedule tasks and routes,
- give customers real-time visibility,
- analyze performance and profitability.

## Features

- work order dashboard with search and filters,
- create, edit, and delete orders,
- client and site data,
- technician assignment and scheduling,
- status tracking and progress,
- photo and file attachments,
- user roles and permissions,
- export-ready reporting,
- AI-ready dispatch layer.

## Stack

- Backend: Python, FastAPI, SQLAlchemy
- Frontend: React, TypeScript, Vite, Tailwind-inspired CSS
- Database: SQLite for local MVP, PostgreSQL-ready for production
- Containerization: Docker / Docker Compose

## Quick start

### Local backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Local frontend

```bash
cd frontend
npm install
npm run dev -- --host
```

Then open:

```text
http://localhost:5173
```

### Docker

```bash
docker-compose up --build
```

## Default demo data

The system seeds sample work orders so the dashboard is useful immediately.

## Product positioning

FieldFlow AI is designed for:
- service companies,
- field service teams,
- maintenance and repair businesses,
- cleaning and janitorial operations,
- HVAC and plumbing contractors,
- technical support teams,
- facility management and property service providers.

## Business model

This is a SaaS product with recurring revenue and services revenue:
- subscription plans,
- team and enterprise plans,
- white-label deployments,
- onboarding and setup services,
- custom integrations.

## Project notes

This repository is a working MVP structure for a service work order SaaS platform. It is intentionally built to be easy to extend into a full production product.

## Contact

- Email: ki9521787@gmail.com
- Website: https://fieldflowai.com
- GitHub: https://github.com/ki9521787ki9521787/fieldflow-ai
