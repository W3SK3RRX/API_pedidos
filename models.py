from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from database import metadata

Base = declarative_base(metadata=metadata)

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    opening_hours = Column(String, nullable=True)
    contact_info = Column(String, nullable=True)

    # Relacionamento com MenuItem (um para muitos)
    menu_items = relationship("MenuItemSQL", back_populates="restaurant")

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

    # Chave estrangeira para vincular o item ao restaurante
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship("Restaurant", back_populates="menu_items")
