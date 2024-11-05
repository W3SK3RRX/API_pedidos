from pydantic import BaseModel
from typing import List, Dict, Optional

class RestaurantBase(BaseModel):
    name: str
    address: str
    opening_hours: Optional[str] = None
    contact_info: Optional[str] = None

# Schema para criação de um restaurante
class RestaurantCreate(RestaurantBase):
    pass

# Schema para leitura de um restaurante, incluindo menu_items
class Restaurant(RestaurantBase):
    id: int
    menu_items: List['MenuItem'] = []

    class Config:
        orm_mode = True

class MenuItem(BaseModel):
    id: Optional[int] = None
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
