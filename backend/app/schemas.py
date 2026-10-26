from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=40)
    email: str = Field(..., min_length=5, max_length=200)
    password: str = Field(..., min_length=6, max_length=128)
    role: str = "operator"

    @field_validator("username")
    @classmethod
    def clean_username(cls, value: str) -> str:
        return value.strip()

    @field_validator("email")
    @classmethod
    def clean_email(cls, value: str) -> str:
        return value.strip().lower()


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool


class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    company: str = Field(default="", max_length=200)
    email: str = Field(default="", max_length=200)
    phone: str = Field(default="", max_length=80)
    city: str = Field(default="", max_length=120)
    notes: str = Field(default="")


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None


class SiteCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    address: str = Field(..., min_length=5, max_length=250)
    city: str = Field(default="", max_length=120)
    timezone: str = Field(default="UTC", max_length=80)
    client_id: Optional[int] = None
    notes: str = Field(default="")


class SiteUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    timezone: Optional[str] = None
    client_id: Optional[int] = None
    notes: Optional[str] = None


class WorkOrderCreate(BaseModel):
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
    client_id: Optional[int] = None
    site_id: Optional[int] = None


class WorkOrderUpdate(BaseModel):
    order_number: Optional[str] = None
    client_name: Optional[str] = None
    site_name: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[str] = None
    scheduled_at: Optional[str] = None
    description: Optional[str] = None
    task_count: Optional[int] = None
    completion_percent: Optional[int] = None
    notes: Optional[str] = None
    client_id: Optional[int] = None
    site_id: Optional[int] = None


class WorkOrderOut(BaseModel):
    id: int
    order_number: str
    client_name: str
    site_name: str
    address: str
    status: str
    priority: str
    assigned_to: str
    scheduled_at: str
    description: str
    task_count: int
    completion_percent: int
    notes: str
    client_id: Optional[int] = None
    site_id: Optional[int] = None
    created_by_id: Optional[int] = None
