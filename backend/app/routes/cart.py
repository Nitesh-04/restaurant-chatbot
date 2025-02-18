from enum import Enum
from fastapi import APIRouter, Depends, HTTPException, Query
from app.database import get_db_connection
from app.auth import require_admin
from pydantic import BaseModel

router = APIRouter()

class CartItem(BaseModel):
    user_id: int
    item_id: int
    quantity: int


@router.get("/item")
def get_item(item_name: str = Query(...), auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM menu WHERE item_name = %s", (item_name,))
        res = cursor.fetchone()
    
    conn.close()
    if not res:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"item_id": res}


@router.get("/{user_id}")
def view_cart(user_id: int, auth: bool = Depends(require_admin)):
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT c.id, c.item_id, m.item_name, c.quantity, m.price FROM cart c JOIN menu m ON c.item_id = m.id WHERE c.user_id = %s",
            (user_id,)
        )
        cart_items = cursor.fetchall()
    
    conn.close()
    return {"cart": cart_items}


@router.post("/")
def add_to_cart(cart_item: CartItem, auth: bool = Depends(require_admin)):

    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO cart (user_id, item_id, quantity) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE quantity = quantity + %s",
            (cart_item.user_id, cart_item.item_id, cart_item.quantity, cart_item.quantity)
        )
        conn.commit()
    
    conn.close()
    return {"message": "Item added to cart"}


class CartAction(str, Enum):
    INCREASE = "increase"
    DECREASE = "decrease"

class CartUpdateRequest(BaseModel):
    user_id: int
    item_id: int
    action: CartAction

@router.patch("/")
def manage_cart_item(update_request: CartUpdateRequest, auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    with conn.cursor() as cursor:
        # Check if item exists in cart
        cursor.execute("SELECT quantity FROM cart WHERE user_id = %s AND item_id = %s", 
                       (update_request.user_id, update_request.item_id))
        item = cursor.fetchone()

        if not item:
            return {"error": "Item not found in cart"}
        
        if update_request.action == CartAction.INCREASE:
            cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE user_id = %s AND item_id = %s", 
                           (update_request.user_id, update_request.item_id))
        else:
            if item["quantity"] > 1:
                cursor.execute("UPDATE cart SET quantity = quantity - 1 WHERE user_id = %s AND item_id = %s", 
                               (update_request.user_id, update_request.item_id))
            else:
                cursor.execute("DELETE FROM cart WHERE user_id = %s AND item_id = %s", 
                               (update_request.user_id, update_request.item_id))

        conn.commit()

    conn.close()
    return {"message": "Cart updated"}


@router.delete("/")
def remove_from_cart(user_id: int, item_id: int, auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM cart WHERE user_id = %s AND item_id = %s", (user_id, item_id))
        conn.commit()

    conn.close()
    return {"message": "Item removed from cart"}
