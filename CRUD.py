from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Base(BaseModel):
    name: str
    price: float
    description: str | None = None
    tax: float | None = None

class ItemCreate(Base):
    pass

class ItemUpdate(Base):
    pass

class Item(Base):
    id :int

item_db = {}
next_id = 1

@app.post("/items/",response_model=Item)
async def create_item(item: ItemCreate):
    global next_id
    new_item = Item(**item.model_dump(), id=next_id)
    item_db[next_id] = new_item
    next_id+=1
    return new_item

@app.get("/items/{item_id}",response_model=Item)
async def read_item(item_id: int):
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_db[item_id]

@app.get("/items/",response_model=list[Item])
async def read_items(skip:int=0,limit:int=10):
    all_items = list(item_db.values())
    return all_items[skip:skip+limit]

@app.put("/items/{item_id}",response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    existing_item = item_db[item_id]
    existing_item.model_update(item.model_dump(exclude_unset=True))
    return existing_item

@app.delete("/items/{item_id}")
async def delete_item(item_id :int):
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del item_db[item_id]
    return {"message": "Item deleted successfully"}
