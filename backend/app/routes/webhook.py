from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
from app.services.orders import add_item, add_order, remove_item, track_order

router = APIRouter()

# Intent to function mapping
INTENT_HANDLERS = {
    "order.add - context:ongoing-order": add_item,
    "order.complete - context:ongoing-order": add_order,
    "order.remove - context:ongoing-order": remove_item,
    "track.order": track_order,
}


@router.post("/")
async def handle_webhook(request: Dict):
    try:
        intent_name = request.get("queryResult", {}).get("intent", {}).get("displayName")
        parameters = request.get("queryResult", {}).get("parameters", {})

        if not intent_name:
            return JSONResponse(content={"fulfillmentText": "Sorry, I couldn't understand that."})

        handler = INTENT_HANDLERS.get(intent_name)
        if handler:
            return await handler(parameters)

        return JSONResponse(content={"fulfillmentText": "I'm sorry, I didn't understand that."})

    except Exception as e:
        return JSONResponse(content={"fulfillmentText": "An error occurred while processing your request."})
