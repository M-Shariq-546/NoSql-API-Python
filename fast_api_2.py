from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    address = Column(String)

    orders = relationship("Order", back_populates="customer")

# Define the Order model
class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date)
    total_amount = Column(Float)

    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    customer = relationship("Customer", back_populates="orders")

# Create the tables in the database
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello World"}

# Create a sessionmaker to handle database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Insert a new customer into the database
@app.post("/customers/")
async def create_customer(name: str, email: str, address: str):
    db = SessionLocal()
    customer = Customer(name="Muhammad Ali", email="Ali888@gmail.com", address="Lahore Pakistan")
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

# Insert a new order into the database for a given customer
@app.post("/customers/{customer_id}/orders/")
async def create_order(customer_id: int, order_date: str, total_amount: float):
    db = SessionLocal()
    order = Order(order_date="29/3/23", total_amount=99.9, customer_id=2)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
