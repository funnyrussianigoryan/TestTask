from datetime import datetime

from sqlalchemy.orm import declarative_base

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
    Boolean,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)


class CurrentSalary(Base):
    __tablename__ = "current_salary"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey(User.id), nullable=False, unique=True)
    created_by = Column(ForeignKey(User.id), nullable=False)
    salary = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)


class SalaryIncrease(Base):
    __tablename__ = "salary_increase"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(ForeignKey(User.id), nullable=False, unique=True)
    created_by = Column(ForeignKey(User.id), nullable=False)
    new_salary = Column(Integer, nullable=False)
    increase_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
