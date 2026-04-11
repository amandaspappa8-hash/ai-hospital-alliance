from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    hospital_id = Column(String)

class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(String, primary_key=True)
    name = Column(String)
