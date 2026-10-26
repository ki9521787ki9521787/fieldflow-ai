from typing import Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Client, Site, User, WorkOrder
from app.schemas import ClientCreate, ClientUpdate, SiteCreate, SiteUpdate, UserCreate, WorkOrderCreate, WorkOrderUpdate
from app.security import hash_password


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    user = User(
        username=payload.username.strip(),
        email=payload.email.strip().lower(),
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def list_orders(db: AsyncSession):
    result = await db.execute(select(WorkOrder).order_by(WorkOrder.created_at.desc()))
    return result.scalars().all()


async def get_order(db: AsyncSession, order_id: int):
    return await db.get(WorkOrder, order_id)


async def create_order(db: AsyncSession, order: WorkOrderCreate, created_by_id: int | None = None):
    db_order = WorkOrder(**order.model_dump(), created_by_id=created_by_id)
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


async def list_clients(db: AsyncSession):
    result = await db.execute(select(Client).order_by(Client.created_at.desc()))
    return result.scalars().all()


async def get_client(db: AsyncSession, client_id: int):
    return await db.get(Client, client_id)


async def create_client(db: AsyncSession, payload: ClientCreate):
    row = Client(**payload.model_dump())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def update_client(db: AsyncSession, existing: Client, payload: ClientUpdate):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_client(db: AsyncSession, client: Client):
    await db.delete(client)
    await db.commit()
    return True


async def list_sites(db: AsyncSession):
    result = await db.execute(select(Site).order_by(Site.created_at.desc()))
    return result.scalars().all()


async def get_site(db: AsyncSession, site_id: int):
    return await db.get(Site, site_id)


async def create_site(db: AsyncSession, payload: SiteCreate):
    row = Site(**payload.model_dump())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def update_site(db: AsyncSession, existing: Site, payload: SiteUpdate):
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(existing, key, value)
    await db.commit()
    await db.refresh(existing)
    return existing


async def delete_site(db: AsyncSession, site: Site):
    await db.delete(site)
    await db.commit()
    return True


async def count_records(db: AsyncSession) -> dict[str, int]:
    orders = await db.scalar(select(func.count()).select_from(WorkOrder)) or 0
    clients = await db.scalar(select(func.count()).select_from(Client)) or 0
    sites = await db.scalar(select(func.count()).select_from(Site)) or 0
    users = await db.scalar(select(func.count()).select_from(User)) or 0
    return {"orders": int(orders), "clients": int(clients), "sites": int(sites), "users": int(users)}
