from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import HTTPException
from pydantic import BaseModel, Field


class LoginForm(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class CreateOrderDraft(BaseModel):
    order_number: str = Field(..., min_length=2)
    client_name: str = Field(..., min_length=2)
    site_name: str = Field(..., min_length=2)
    address: str = Field(..., min_length=2)
    status: str = "new"
    priority: str = "normal"
    assigned_to: str = "Unassigned"
    scheduled_at: str = ""
    description: str = ""
    task_count: int = Field(default=0, ge=0)
    completion_percent: int = Field(default=0, ge=0, le=100)
    notes: str = ""


DEFAULT_DEMO_USER = {
    "username": "admin",
    "password": "admin123",
    "email": "admin@fieldflow.ai",
}


def normalize_order_status(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "_")
    allowed = {"new", "scheduled", "in_progress", "completed", "on_hold"}
    if normalized not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported status: {value}")
    return normalized


def normalize_priority(value: str) -> str:
    normalized = value.strip().lower()
    allowed = {"normal", "high", "urgent"}
    if normalized not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported priority: {value}")
    return normalized


def upcoming_service_date(days_from_now: int = 7) -> str:
    return (datetime.utcnow() + timedelta(days=days_from_now)).strftime("%Y-%m-%d")
