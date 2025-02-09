from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db_connection
from app.auth import require_admin
from pydantic import BaseModel

router = APIRouter()

class CartItem(BaseModel):
    user_id: int
    item_id: int
    quantity: int


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


@router.patch("/{cart_id}")
def update_cart(cart_id: int, quantity: int, auth: bool = Depends(require_admin)):

    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    with conn.cursor() as cursor:
        cursor.execute("UPDATE cart SET quantity = %s WHERE id = %s", (quantity, cart_id))
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
