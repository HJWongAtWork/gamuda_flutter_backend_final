from sqlalchemy import Column, DateTime, Float, Integer, String
from app.config.database import Base

class User(Base):
    """Database model for users."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    city = Column(String)
    salary = Column(Float)
    join_date = Column(DateTime)

class Account(Base):
    """Database model for user accounts."""
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)  # Made nullable for social login
    social_id = Column(String, unique=True, nullable=True)
    social_provider = Column(String, nullable=True)
