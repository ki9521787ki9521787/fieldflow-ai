from datetime import datetime

from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    client_name: Mapped[str] = mapped_column(String(200), nullable=False)
    site_name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[str] = mapped_column(String(400), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="new")
    priority: Mapped[str] = mapped_column(String(50), default="normal")
    assigned_to: Mapped[str] = mapped_column(String(200), default="Unassigned")
    scheduled_at: Mapped[str] = mapped_column(String(50), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    task_count: Mapped[int] = mapped_column(Integer, default=0)
    completion_percent: Mapped[int] = mapped_column(Integer, default=0)
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_number": self.order_number,
            "client_name": self.client_name,
            "site_name": self.site_name,
            "address": self.address,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "scheduled_at": self.scheduled_at,
            "description": self.description,
            "task_count": self.task_count,
            "completion_percent": self.completion_percent,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
