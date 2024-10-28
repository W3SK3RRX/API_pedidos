from sqlalchemy import Column, Integer, String, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import List, Dict
from database import metadata

Base = declarative_base(metadata=metadata)

class MenuItemSQL(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    available = Column(Boolean)
    category = Column(String)
    image_url = Column(String)
    preparation_time = Column(Integer)
    ingredients = Column(JSON)
    options = Column(JSON)

class MenuItem(BaseModel):
    id: int
    name: str
    description: str
    price: float
    available: bool
    category: str
    image_url: str
    preparation_time: int
    ingredients: List[str]
    options: List[Dict]

    class Config:
        orm_mode = True
