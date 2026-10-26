from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SECRET_KEY = "ki9521787-real-production-secret-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

SQLALCHEMY_DATABASE_URL = "sqlite:///./fieldflow.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="OPERATOR")
    owner = Column(String, default="ki9521787@gmail.com")


class OrderDB(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    client = Column(String, index=True)
    system = Column(String)
    status = Column(String, default="Pending")
    priority = Column(String, default="Medium")
    technician = Column(String, default="Unassigned")


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FieldFlow AI Production API",
    version="2.1.0",
    description="Created and owned by ki9521787@gmail.com",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = SessionLocal()
    admin = db.query(UserDB).filter(UserDB.email == "admin@fieldflowai.com").first()
    if not admin:
        db_user = UserDB(
            email="admin@fieldflowai.com",
            hashed_password=pwd_context.hash("admin123"),
            role="ADMIN",
            owner="ki9521787@gmail.com",
        )
        db.add(db_user)
        db.commit()
    if db.query(OrderDB).count() == 0:
        db.add(
            OrderDB(
                id="WO-1001",
                client="Apex Commercial Ltd",
                system='Domestic Cold Water - 2" Copper',
                status="In Progress",
                priority="High",
                technician="Alex R.",
            )
        )
        db.add(
            OrderDB(
                id="WO-1002",
                client="Metro Plaza Facility",
                system='Sanitary Waste - Cast Iron 4"',
                status="Pending",
                priority="Medium",
                technician="Unassigned",
            )
        )
        db.commit()
    db.close()


init_db()


class OrderCreate(BaseModel):
    client: str
    system: str
    priority: Optional[str] = "Medium"


@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user or not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Неверный email или пароль")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": user.email, "role": user.role, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer", "role": user.role, "owner": "ki9521787@gmail.com"}


@app.get("/api/orders")
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(OrderDB).all()
    return {"status": "success", "owner": "ki9521787@gmail.com", "data": orders}


@app.post("/api/orders")
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    count = db.query(OrderDB).count()
    new_id = f"WO-10{count + 1}"
    db_order = OrderDB(
        id=new_id,
        client=order.client,
        system=order.system,
        status="Pending",
        priority=order.priority,
        technician="Assigned Dispatch",
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return {"status": "created", "order": db_order, "owner": "ki9521787@gmail.com"}


@app.get("/health")
async def health():
    return {"status": "operational", "owner": "ki9521787@gmail.com"}
