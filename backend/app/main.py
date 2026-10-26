from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud import create_order, delete_order, get_order, list_orders, update_order
from app.database import get_db, init_db
from app.models import WorkOrder
from app.schemas import WorkOrderCreate, WorkOrderUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="FieldFlow AI", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(',') if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "fieldflow-ai"}


@app.get("/api/orders")
async def read_orders(db: AsyncSession = Depends(get_db)):
    orders = await list_orders(db)
    return [order.to_dict() for order in orders]


@app.get("/api/orders/{order_id}")
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.to_dict()


@app.post("/api/orders", status_code=status.HTTP_201_CREATED)
async def create_new_order(payload: WorkOrderCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(WorkOrder).where(WorkOrder.order_number == payload.order_number))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Order number already exists")
    order = await create_order(db, payload)
    return order.to_dict()


@app.put("/api/orders/{order_id}")
async def update_existing_order(order_id: int, payload: WorkOrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    updated = await update_order(db, order, payload)
    return updated.to_dict()


@app.delete("/api/orders/{order_id}")
async def delete_existing_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await delete_order(db, order)
    return {"deleted": True, "id": order_id}


@app.get("/api/metrics")
async def read_metrics(db: AsyncSession = Depends(get_db)):
    orders = await list_orders(db)
    total = len(orders)
    active = sum(1 for order in orders if order.status in {"new", "scheduled", "in_progress"})
    urgent = sum(1 for order in orders if order.priority == "urgent")
    completed = sum(1 for order in orders if order.status == "completed")
    return {
        "total": total,
        "active": active,
        "urgent": urgent,
        "completed": completed,
    }
