from fastapi import FastAPI, HTTPException, Depends
from typing import List
from schemas import MenuItem, Restaurant, RestaurantCreate
from models import MenuItemSQL, Restaurant as RestaurantSQL
from database import database
from sqlalchemy import select


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def root():
    return {"Pedidos":"Delivery"}


# Rotas para restaurante

#criar restaurante
@app.post("/restaurants/", response_model=Restaurant)
async def create_restaurant(restaurant: RestaurantCreate):
    query = RestaurantSQL.__table__.insert().values(
        name=restaurant.name,
        address=restaurant.address,
        opening_hours=restaurant.opening_hours,
        contact_info=restaurant.contact_info,
    )
    restaurant_id = await database.execute(query)
    return {**restaurant.dict(), "id": restaurant_id}

#Listar todos os restaurantes
@app.get("/restaurants/", response_model=List[Restaurant])
async def get_restaurabts():
    query = select(RestaurantSQL)
    results = await database.fetch_all(query)
    return results

#Buscar restaurante pelo ID
@app.get("/restaurants/{restaurant_id}", response_model=Restaurant)
async def get_restaurant(restaurant_id: int):
    query = select(RestaurantSQL).where(RestaurantSQL.id == restaurant_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return result

# Criar um novo item de menu associado a um restaurante
@app.post("/restaurants/{restaurant_id}/menu_items/", response_model=MenuItem)
async def create_menu_item(restaurant_id: int, item: MenuItem):
    # Verificar se o restaurante existe
    restaurant_query = select(RestaurantSQL).where(RestaurantSQL.id == restaurant_id)
    restaurant = await database.fetch_one(restaurant_query)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Criar item de menu
    query = MenuItemSQL.__table__.insert().values(
        name=item.name,
        description=item.description,
        price=item.price,
        available=item.available,
        category=item.category,
        image_url=item.image_url,
        preparation_time=item.preparation_time,
        ingredients=str(item.ingredients),
        options=str(item.options),
        restaurant_id=restaurant_id
    )
    item_id = await database.execute(query)
    return {**item.dict(), "id": item_id, "restaurant_id": restaurant_id}

# Listar todos os itens de menu de um restaurante específico
@app.get("/restaurants/{restaurant_id}/menu_items/", response_model=List[MenuItem])
async def get_menu_items(restaurant_id: int):
    # Verificar se o restaurante existe
    restaurant_query = select(RestaurantSQL).where(RestaurantSQL.id == restaurant_id)
    restaurant = await database.fetch_one(restaurant_query)
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    query = select(MenuItemSQL).where(MenuItemSQL.restaurant_id == restaurant_id)
    results = await database.fetch_all(query)
    
    menu_items = []
    for result in results:
        item = dict(result)
        item["ingredients"] = eval(item["ingredients"]) if item["ingredients"] else []
        item["options"] = eval(item["options"]) if item["options"] else []
        menu_items.append(item)
    
    return menu_items


# Buscar item de menu pelo ID e pelo restaurante
@app.get("/restaurants/{restaurant_id}/menu_items/{item_id}", response_model=MenuItem)
async def get_menu_item(restaurant_id: int, item_id: int):
    query = select(MenuItemSQL).where(MenuItemSQL.id == item_id, MenuItemSQL.restaurant_id == restaurant_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    item = dict(result)
    item["ingredients"] = eval(item["ingredients"]) if item["ingredients"] else []
    item["options"] = eval(item["options"]) if item["options"] else []
    
    return item


# Atualizar item de menu específico de um restaurante
@app.put("/restaurants/{restaurant_id}/menu_items/{item_id}", response_model=MenuItem)
async def update_menu_item(restaurant_id: int, item_id: int, updated_item: MenuItem):
    # Verificar se o item existe
    select_query = select(MenuItemSQL).where(MenuItemSQL.id == item_id)
    existing_item = await database.fetch_one(select_query)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")

    # Atualizar o item de menu
    update_query = (
        MenuItemSQL.__table__.update()
        .where(MenuItemSQL.id == item_id)
        .values(
            name=updated_item.name,
            description=updated_item.description,
            price=updated_item.price,
            available=updated_item.available,
            category=updated_item.category,
            image_url=updated_item.image_url,
            preparation_time=updated_item.preparation_time,
            ingredients=str(updated_item.ingredients),
            options=str(updated_item.options)
        )
    )
    await database.execute(update_query)
    # Retornar o item atualizado com o `restaurant_id`
    return {**updated_item.dict(), "id": item_id, "restaurant_id": existing_item["restaurant_id"]}


# Deletar item de menu específico de um restaurante
@app.delete("/restaurants/{restaurant_id}/menu_items/{item_id}")
async def delete_menu_item(restaurant_id: int, item_id: int):
    # Verificar se o item existe
    select_query = select(MenuItemSQL).where(MenuItemSQL.id == item_id)
    existing_item = await database.fetch_one(select_query)
    if existing_item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    
    # Deletar o item de menu
    delete_query = MenuItemSQL.__table__.delete().where(MenuItemSQL.id == item_id)
    await database.execute(delete_query)
    return {"message": "Item deleted successfully"}
