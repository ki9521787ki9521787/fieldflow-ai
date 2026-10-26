from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import WorkOrder
from app.schemas import WorkOrderCreate, WorkOrderUpdate


async def list_orders(db: AsyncSession):
    result = await db.execute(select(WorkOrder).order_by(WorkOrder.created_at.desc()))
    return result.scalars().all()


async def get_order(db: AsyncSession, order_id: int):
    return await db.get(WorkOrder, order_id)


async def create_order(db: AsyncSession, order: WorkOrderCreate):
    db_order = WorkOrder(**order.model_dump())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def update_order(db: AsyncSession, existing: WorkOrder, payload: WorkOrderUpdate):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_order(db: AsyncSession, order: WorkOrder):
    await db.delete(order)
    await db.commit()
    return True
