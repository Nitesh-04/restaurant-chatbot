from typing import Dict
from fastapi.responses import JSONResponse
import os
import httpx

admin_key = os.getenv("ADMIN_KEY")


async def add_item(parameters: Dict):
    item_names = parameters.get("food-item",[])
    quantities = parameters.get("number",[])

    if len(item_names) != len(quantities):
        return JSONResponse(content={"fulfillmentText": "Please specify a quantity for each item."})
    
    added_items = []  

    async with httpx.AsyncClient() as client:
        for item_name, quantity in zip(item_names, quantities):
            if not item_name or not quantity:
                continue
            try:
                response = await client.post(
                    "http://localhost:8000/cart",
                    json={"user_id": 11, "item_name": item_name, "quantity": quantity},
                    headers={"admin-key": admin_key}
                )
                response.raise_for_status()

                response_data = response.json()
                if response_data.get("status") == "success":
                    added_items.append(f"{quantity}x {item_name}")
                else:
                    return JSONResponse(content={"fulfillmentText": "Failed to add items to cart."})

            except httpx.HTTPStatusError:
                return JSONResponse(content={"fulfillmentText": "Failed to add items to cart."})

            
async def add_order():

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/order",
                json={"user_id": 11},
                headers={"admin-key": admin_key}
            )
            response.raise_for_status()

            response_data = response.json()
            if response_data.get("status") == "success":
                return JSONResponse(content={"fulfillmentText": "Order placed successfully."})
            else:
                return JSONResponse(content={"fulfillmentText": "Failed to place order."})

    except httpx.HTTPStatusError:
        return JSONResponse(content={"fulfillmentText": "Failed to place order."})


async def remove_item(parameters: Dict):
    item_name = parameters.get("food-item")
    quantity = parameters.get("number")

    if not item_name or not quantity:
        return JSONResponse(content={"fulfillmentText": "Please specify a valid item and quantity."})
    
    try:
        async with httpx.AsyncClient() as client:
            fetch_response = await client.get(
                "http://127.0.0.1:8000/cart/",
                params={"item_name": item_name},
                headers={"admin-key": admin_key}
            )
            fetch_response.raise_for_status()
            fetch_data = fetch_response.json()
            item_id = fetch_data.get("item_id")

            if not item_id:
                return JSONResponse(content={"fulfillmentText": "Item not found in cart."})
    
    except httpx.HTTPStatusError:
        return JSONResponse(content={"fulfillmentText": "Failed to remove item from cart."})

    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                "http://localhost:8000/cart",
                json={"user_id": 11, "item_id": item_id, "quantity": quantity},
                headers={"admin-key": admin_key}
            )
            response.raise_for_status()

            response_data = response.json()
            if response_data.get("status") == "success":
                return JSONResponse(content={"fulfillmentText": f"{quantity}x {item_name} removed from cart."})
            else:
                return JSONResponse(content={"fulfillmentText": "Failed to remove item from cart."})

    except httpx.HTTPStatusError:
        return JSONResponse(content={"fulfillmentText": "Failed to remove item from cart."})


async def track_order(parameters: Dict):
    order_id = parameters.get("order-id")

    if not order_id:
        return JSONResponse(content={"fulfillmentText": "Please provide a valid order ID."})

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8000/track/{order_id}", headers={"admin-key": admin_key})
            response.raise_for_status()
            response_data = response.json()
            order_status = response_data.get("status", "unknown")

            return JSONResponse(content={"fulfillmentText": f"Order {order_id} is {order_status}."})

    except httpx.HTTPStatusError as e:
        return JSONResponse(content={"fulfillmentText": f"Failed to fetch order status."})

    except Exception as e:
        return JSONResponse(content={"fulfillmentText": "An unexpected error occurred while tracking the order."})
