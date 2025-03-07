from fastapi import APIRouter
from app.api.api_v1.endpoints import users, inventory, sales, purchase

api_router = APIRouter()
api_router.include_router(users.router, tags=["users"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(purchase.router, prefix="/purchase", tags=["purchase"]) 