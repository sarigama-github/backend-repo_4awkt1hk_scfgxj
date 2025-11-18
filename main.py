import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Pizza, Order

app = FastAPI(title="Pizzeria API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Pizzeria backend beží"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

# Utilities
class PizzaOut(BaseModel):
    id: str
    name: str
    description: str | None = None
    price: float
    size: str
    vegetarian: bool
    spicy: bool
    image: str | None = None

    @staticmethod
    def from_mongo(doc: dict) -> "PizzaOut":
        return PizzaOut(
            id=str(doc.get("_id")),
            name=doc.get("name"),
            description=doc.get("description"),
            price=float(doc.get("price")),
            size=doc.get("size"),
            vegetarian=bool(doc.get("vegetarian")),
            spicy=bool(doc.get("spicy")),
            image=doc.get("image")
        )

# Endpoints: Menu
@app.get("/api/pizzas", response_model=List[PizzaOut])
def list_pizzas():
    docs = get_documents("pizza")
    return [PizzaOut.from_mongo(d) for d in docs]

@app.post("/api/pizzas")
def create_pizza(pizza: Pizza):
    new_id = create_document("pizza", pizza)
    return {"id": new_id}

# Endpoints: Orders
@app.post("/api/orders")
def create_order(order: Order):
    new_id = create_document("order", order)
    return {"id": new_id}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
