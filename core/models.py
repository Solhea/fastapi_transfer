from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT, DECIMAL
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True)
    password = Column(String(255))
    firstName = Column(String(50))
    lastName = Column(String(50))
    is_active = Column(Boolean, default=True)


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    address = Column(String(50))
    lat = Column(DECIMAL(10, 8))
    lng = Column(DECIMAL(11, 8))
    is_picked = Column(Boolean, default=False)
    operation_id = Column(Integer, ForeignKey("operations.id"))
    operation = relationship("Operation", back_populates="employees")


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(50))
    phone = Column(String(50))
    address = Column(String(50))
    lat = Column(DECIMAL(10, 8))
    lng = Column(DECIMAL(11, 8))
    on_operation = Column(Boolean, default=False)
    license_plate = Column(String(50))
    operations = relationship("Operation", back_populates="driver")


class Operation(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(LONGTEXT)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, default=datetime.utcnow)
    is_finished = Column(Boolean, default=False)

    employees = relationship(
        "Employee", back_populates="operations", lazy="joined")
    driver = relationship("Driver", back_populates="operations", lazy="joined")
