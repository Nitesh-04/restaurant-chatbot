from fastapi import APIRouter,Depends,HTTPException
from typing import Dict
from fastapi.responses import JSONResponse
import os
import httpx

router = APIRouter()

async def handle_add_order(parameters: Dict):
    item_name = parameters.get("food-item")
    quantity = parameters.get("number")

    #add logic to handle the order like saving to DB

    return JSONResponse(content={"fulfillmentText": f"{quantity} x {item_name} added to cart."})


async def handle_remove_order(parameters: Dict):
    item_name = parameters.get("food-item")

    #add logic to handle the removal, such as checking the DB

    return JSONResponse(content={"fulfillmentText": f"{item_name} removed from cart."})

async def handle_track_order(parameters: Dict):

    admin_key = os.getenv("ADMIN_KEY")
    order_id = parameters.get("order-id")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/track/{order_id}", headers={"admin-key": admin_key})
        response_data = response.json()

    order_status = response_data.get("status")

    return JSONResponse(content={"fulfillmentText": f"Order {order_id} is {order_status}."})
    