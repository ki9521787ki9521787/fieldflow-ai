from datetime import datetime, timedelta

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import WorkOrder


async def seed_demo_data() -> None:
    async with AsyncSessionLocal() as db:
        existing = await db.execute(select(WorkOrder).limit(1))
        if existing.scalar_one_or_none() is not None:
            return

        samples = [
            {
                "order_number": "FF-1001",
                "client_name": "Apex Facilities",
                "site_name": "North Tower",
                "address": "15 Harbor Avenue, Seattle, WA",
                "status": "in_progress",
                "priority": "urgent",
                "assigned_to": "Maya Chen",
                "scheduled_at": (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "description": "HVAC inspection and filter replacement.",
                "task_count": 4,
                "completion_percent": 65,
                "notes": "Customer requested same-day report follow-up.",
            },
            {
                "order_number": "FF-1002",
                "client_name": "UrbanLiving Homes",
                "site_name": "Elm Residences",
                "address": "821 Pine Street, Portland, OR",
                "status": "scheduled",
                "priority": "normal",
                "assigned_to": "Leo Rivera",
                "scheduled_at": (datetime.utcnow() + timedelta(days=2)).strftime("%Y-%m-%d"),
                "description": "Plumbing maintenance for three residential units.",
                "task_count": 3,
                "completion_percent": 30,
                "notes": "Need access to unit 3B before 10 AM.",
            },
            {
                "order_number": "FF-1003",
                "client_name": "Northstar Realty",
                "site_name": "City Center Office",
                "address": "500 8th Avenue, San Diego, CA",
                "status": "new",
                "priority": "high",
                "assigned_to": "Unassigned",
                "scheduled_at": (datetime.utcnow() + timedelta(days=3)).strftime("%Y-%m-%d"),
                "description": "Electrical diagnostics and lighting calibration.",
                "task_count": 5,
                "completion_percent": 5,
                "notes": "Need completion within 48 hours.",
            },
        ]

        db.add_all(WorkOrder(**sample) for sample in samples)
        await db.commit()


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_demo_data())
