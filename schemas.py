"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Pizzeria schemas

class Pizza(BaseModel):
    """
    Pizza collection schema
    Collection name: "pizza"
    """
    name: str = Field(..., description="Pizza name")
    description: Optional[str] = Field(None, description="Short description")
    price: float = Field(..., ge=0, description="Price in EUR")
    size: str = Field("33 cm", description="Default size label")
    vegetarian: bool = Field(False, description="Is vegetarian")
    spicy: bool = Field(False, description="Is spicy")
    image: Optional[str] = Field(None, description="Image URL")

class OrderItem(BaseModel):
    pizza_id: str = Field(..., description="Referenced Pizza document _id as string")
    name: str = Field(..., description="Pizza name at time of order")
    price: float = Field(..., ge=0, description="Unit price at time of order")
    quantity: int = Field(1, ge=1, description="Quantity")

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    customer_name: str = Field(..., description="Customer full name")
    phone: str = Field(..., description="Contact phone number")
    address: str = Field(..., description="Delivery address")
    items: List[OrderItem] = Field(..., description="Ordered items")
    note: Optional[str] = Field(None, description="Optional note for the kitchen or courier")
    total: float = Field(..., ge=0, description="Total amount in EUR")

# Example schemas (kept for reference)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
