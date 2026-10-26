from typing import Optional

from pydantic import BaseModel, Field


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
    task_count: int = 0
    completion_percent: int = 0
    notes: str = ""


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
