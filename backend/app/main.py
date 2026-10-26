from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.crud import (
    create_client,
    create_order,
    create_site,
    create_user,
    delete_client,
    delete_order,
    delete_site,
    get_client,
    get_order,
    get_site,
    get_user_by_email,
    get_user_by_username,
    list_clients,
    list_orders,
    list_sites,
    update_client,
    update_order,
    update_site,
)
from app.database import AsyncSessionLocal, get_db, init_db
from app.models import Client, Site, User, WorkOrder
from app.schemas import (
    ClientCreate,
    ClientUpdate,
    SiteCreate,
    SiteUpdate,
    Token,
    UserCreate,
    UserLogin,
    UserOut,
    WorkOrderCreate,
    WorkOrderUpdate,
)
from app.security import create_access_token, decode_access_token, hash_password, verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with AsyncSessionLocal() as db:
        user_count = await db.scalar(select(func.count()).select_from(User)) or 0
        if user_count == 0:
            default_user = User(
                username="admin",
                email="admin@fieldflow.ai",
                password_hash=hash_password("admin123"),
                role="admin",
                is_active=True,
            )
            db.add(default_user)
            await db.commit()

        order_count = await db.scalar(select(func.count()).select_from(WorkOrder)) or 0
        if order_count == 0:
            demo_orders = [
                WorkOrder(
                    order_number="FF-1001",
                    client_name="Apex Facilities",
                    site_name="North Tower",
                    address="15 Harbor Avenue, Seattle, WA",
                    status="in_progress",
                    priority="urgent",
                    assigned_to="Maya Chen",
                    scheduled_at="2026-11-02",
                    description="HVAC inspection and filter replacement.",
                    task_count=4,
                    completion_percent=68,
                    notes="Customer requested same day follow-up.",
                    created_by_id=1,
                ),
                WorkOrder(
                    order_number="FF-1002",
                    client_name="UrbanLiving Homes",
                    site_name="Elm Residences",
                    address="821 Pine Street, Portland, OR",
                    status="scheduled",
                    priority="normal",
                    assigned_to="Leo Rivera",
                    scheduled_at="2026-11-04",
                    description="Plumbing maintenance and emergency inspection.",
                    task_count=3,
                    completion_percent=35,
                    notes="Access required before 10:00 AM.",
                    created_by_id=1,
                ),
                WorkOrder(
                    order_number="FF-1003",
                    client_name="Northstar Realty",
                    site_name="City Center Office",
                    address="500 8th Avenue, San Diego, CA",
                    status="new",
                    priority="high",
                    assigned_to="Unassigned",
                    scheduled_at="2026-11-06",
                    description="Electrical diagnostics and lighting calibration.",
                    task_count=5,
                    completion_percent=12,
                    notes="Need completion within 48 hours.",
                    created_by_id=1,
                ),
            ]
            db.add_all(demo_orders)
            await db.commit()
    yield


app = FastAPI(
    title="FieldFlow AI",
    version="1.0.0",
    description="Service operations platform for field service companies.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except ValueError as exc:
        raise credentials_exception from exc

    user = await get_user_by_username(db, username)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "fieldflow-ai", "version": "1.0.0"}


@app.post("/api/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    if await get_user_by_username(db, payload.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if await get_user_by_email(db, payload.email):
        raise HTTPException(status_code=400, detail="Email already exists")

    user = await create_user(db, payload)
    return UserOut(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
    )


@app.post("/api/auth/login", response_model=Token)
async def login_user(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, payload.username)
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.username, "user_id": user.id, "role": user.role})
    return Token(access_token=token)


@app.get("/api/auth/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
    )


@app.get("/api/orders")
async def read_orders(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = await list_orders(db)
    return [order.to_dict() for order in orders]


@app.get("/api/orders/{order_id}")
async def read_order(order_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order.to_dict()


@app.post("/api/orders", status_code=status.HTTP_201_CREATED)
async def create_new_order(payload: WorkOrderCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = await db.execute(select(WorkOrder).where(WorkOrder.order_number == payload.order_number))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Order number already exists")
    order = await create_order(db, payload, created_by_id=current_user.id)
    return order.to_dict()


@app.put("/api/orders/{order_id}")
async def update_existing_order(order_id: int, payload: WorkOrderUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    updated = await update_order(db, order, payload)
    return updated.to_dict()


@app.delete("/api/orders/{order_id}")
async def delete_existing_order(order_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = await get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    await delete_order(db, order)
    return {"deleted": True, "id": order_id}


@app.get("/api/clients")
async def read_clients(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    clients = await list_clients(db)
    return [client.to_dict() for client in clients]


@app.post("/api/clients", status_code=status.HTTP_201_CREATED)
async def create_new_client(payload: ClientCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = await create_client(db, payload)
    return client.to_dict()


@app.put("/api/clients/{client_id}")
async def update_existing_client(client_id: int, payload: ClientUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = await get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    updated = await update_client(db, client, payload)
    return updated.to_dict()


@app.delete("/api/clients/{client_id}")
async def delete_existing_client(client_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    client = await get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    await delete_client(db, client)
    return {"deleted": True, "id": client_id}


@app.get("/api/sites")
async def read_sites(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    sites = await list_sites(db)
    return [site.to_dict() for site in sites]


@app.post("/api/sites", status_code=status.HTTP_201_CREATED)
async def create_new_site(payload: SiteCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    site = await create_site(db, payload)
    return site.to_dict()


@app.put("/api/sites/{site_id}")
async def update_existing_site(site_id: int, payload: SiteUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    site = await get_site(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    updated = await update_site(db, site, payload)
    return updated.to_dict()


@app.delete("/api/sites/{site_id}")
async def delete_existing_site(site_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    site = await get_site(db, site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    await delete_site(db, site)
    return {"deleted": True, "id": site_id}


@app.get("/api/metrics")
async def read_metrics(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = await list_orders(db)
    total = len(orders)
    active = sum(1 for order in orders if order.status in {"new", "scheduled", "in_progress"})
    urgent = sum(1 for order in orders if order.priority == "urgent")
    completed = sum(1 for order in orders if order.status == "completed")
    clients = await list_clients(db)
    sites = await list_sites(db)
    return {
        "total": total,
        "active": active,
        "urgent": urgent,
        "completed": completed,
        "clients": len(clients),
        "sites": len(sites),
    }


@app.get("/api/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    orders = [order.to_dict() for order in await list_orders(db)]
    clients = [client.to_dict() for client in await list_clients(db)]
    sites = [site.to_dict() for site in await list_sites(db)]
    metrics = await read_metrics(db, current_user)
    return {"metrics": metrics, "orders": orders, "clients": clients, "sites": sites, "user": current_user.to_public_dict()}


@app.get("/")
async def root():
    return {"message": "FieldFlow AI API is running."}
