from typing import Dict
from fastapi.responses import JSONResponse

# Function to handle "order.add" intent
async def handle_add_order(parameters: Dict):
    item_name = parameters.get("food-item")
    quantity = parameters.get("number")

    #add logic to handle the order like saving to DB

    return JSONResponse(content={"fulfillmentText": f"{quantity} x {item_name} added to cart."})

# Function to handle "order.remove" intent
async def handle_remove_order(parameters: Dict):
    item_name = parameters.get("food-item")

    #add logic to handle the removal, such as checking the DB

    return JSONResponse(content={"fulfillmentText": f"{item_name} removed from cart."})

async def handle_track_order(parameters: Dict):

    orderId = parameters['order-id']

    #add logic to fetch the order details from the DB

    return JSONResponse(content={"fulfillmentText": f"Received request to track order with ID : {orderId}"})
    