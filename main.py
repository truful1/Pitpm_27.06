from xmlrpc.client import DateTime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import IntegrityError

# Создание объекта FastAPI
app = FastAPI()

# Настройка базы данных MySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://isp_p_Lapin:12345@192.168.25.23/isp_p_Lapin"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Определение модели SQLAlchemy для пользователя
class Online_store(Base):
    __tablename__ = "Online_store"

    store_code = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), index=True)  # Указываем длину для VARCHAR
    payment = Column(Boolean, index=True)  # Указываем длину для VARCHAR

class Product(Base):
    __tablename__ = "product"

    item_code = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    brand = Column(String(50))
    model = Column(String(50))
    specs = Column(String(200))
    price = Column(Integer)
    warranty_period = Column(Integer)
    image = Column(String(200))


class Order(Base):
    __tablename__ = "order"

    order_code = Column(Integer, primary_key=True, index=True)
    store_code = Column(Integer)
    item_code = Column(Integer)
    order_date = Column(String(100))
    order_time = Column(String(100))
    quantity = Column(Integer)
    customer_name = Column(String(100))
    contact_number = Column(String(15))
    confirmation = Column(Boolean)


class Delivery(Base):
    __tablename__ = "delivery"

    order_code = Column(Integer, primary_key=True, index=True)
    delivery_date = Column(String(100))
    delivery_time = Column(String(100))
    delivery_address = Column(String(200))
    customer_name = Column(String(100))
    courier_name = Column(String(100))


# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)


# Определение Pydantic модели для пользователя
class Online_storeCreate(BaseModel):
    email: str
    payment: bool


class Online_storeResponse(BaseModel):
    store_code: int
    email: str
    payment: bool

    class Config:
        orm_mode = True


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Маршрут для получения пользователя по ID
@app.get("/Online_store/{store_code}", response_model=Online_storeResponse)
def read_Online_store(Online_store_store_code: int, db: Session = Depends(get_db)):
    user = db.query(Online_store).filter(Online_store_store_code == Online_store.store_code).first()
    if Online_store is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Online_store


# Маршрут для создания нового пользователя
@app.post("/Online_store/", response_model=Online_storeResponse)
def create_user(user: Online_storeCreate, db: Session = Depends(get_db)):
    db_Online_store = Online_store(email=Online_store.email, payment=Online_store.payment)
    try:
        db.add(db_Online_store)
        db.commit()
        db.refresh(db_Online_store)
        return db_Online_store
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")