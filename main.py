from fastapi import Depends, FastAPI,Query,status,HTTPException, Request
from sqlalchemy import Column,String,Integer, Table, Boolean, Float , Text
from typing import Optional,List, Annotated
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine,sessionLocal,base

app = FastAPI()
base.metadata.create_all(bind=engine)

class Item(base):
    __tablename__ = "first_db"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)    
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    
    
class UserCreate(BaseModel):
    name: str
    description:Optional[str] = None
    price:float    
    
class UserResponse(BaseModel):
    id:int
    name:str
    description:Optional[str] = None
    price:float
    
        


    
    
    
def get_db():
    db = sessionLocal()
    try: 
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# POST: Create a new item
@app.post("/items/", response_model=UserResponse)
def create_item(item: UserCreate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.name == item.name).first()
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists")
    new_item = Item(name=item.name, description=item.description, price=item.price)
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

# GET: Fetch all items
@app.get("/items/", response_model=List[UserResponse])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all()

# GET: Fetch a specific item by ID
@app.get("/items/{item_id}", response_model=UserResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# PUT: Update an item by ID
@app.put("/items/{item_id}", response_model=UserResponse)
def update_item(item_id: int, item: UserCreate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name # type: ignore
    db_item.description = item.description  # type: ignore
    db_item.price = item.price # type: ignore
    db.commit()
    db.refresh(db_item)
    return db_item

# DELETE: Delete an item by ID
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"message": f"Item with ID {item_id} has been deleted."}