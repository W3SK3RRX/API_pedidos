from fastapi import FastAPI, HTTPException
from typing import List
from schemas import MenuItem, MenuItemSQL
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

#rota para criar um novo item
@app.post("/menu_items/")
async def create_menu_item(item: MenuItem):
    query = MenuItemSQL.__table__.insert().values(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        available=item.available,
        category=item.category,
        image_url=item.image_url,
        preparation_time=item.preparation_time,
        ingredients=str(item.ingredients),  # Armazenar como string
        options=str(item.options),  # Armazenar como string
    )
    await database.execute(query)
    return {"message":"Item adicionado com sucesso!", "item":item}


#rota para listar os items
@app.get("/menu/", response_model=List[MenuItem])
async def get_menu_items():
    query = select(MenuItemSQL)
    results = await database.fetch_all(query)
    
    menu_items = []
    for result in results:
        item = dict(result)
        # Converte os campos de string para listas
        item["ingredients"] = eval(item["ingredients"]) if item["ingredients"] else []
        item["options"] = eval(item["options"]) if item["options"] else []
        menu_items.append(item)

    return menu_items


#rota para buscar um item pelo id
@app.get("/menu/{item_id}", response_model=MenuItem)
async def get_menu_item(item_id: int):
    query = select(MenuItemSQL).where(MenuItemSQL.id == item_id)
    result = await database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item = dict(result)
    # Converte os campos de string para listas
    item["ingredients"] = eval(item["ingredients"]) if item["ingredients"] else []
    item["options"] = eval(item["options"]) if item["options"] else []
    
    return item


#rota para atualizar o item pelo id
@app.put("/menu/{item_id}", response_model=MenuItem)
async def update_menu_item(item_id: int, updated_item: MenuItem):
    query = MenuItemSQL.__table__.update().where(MenuItemSQL.id == item_id).values(
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

    result = await database.execute(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

#rota para deletar um item pelo id
@app.delete("/menu/{item_id}")
async def delete_menu_item(item_id:int):
    query = MenuItemSQL.__table__.delete().where(MenuItemSQL.id == item_id)
    result = await database.execute(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
    