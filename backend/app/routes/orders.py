from fastapi import APIRouter,Depends
from app.database import get_db_connection
from app.auth import require_admin
from pydantic import BaseModel

router = APIRouter()

@router.get("/")
def get_orders(auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()
    
    conn.close()
    return {"orders": orders}


@router.get("/{order_id}")
def get_order(order_id: int, auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
    
    conn.close()
    
    if not order:
        return {"error": "Order not found"}
    
    return {"order": order}


class OrderCreate(BaseModel):
    user_id: int
    item_id: int
    quantity: int


@router.post("/")
def create_order(order: OrderCreate, auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO orders (user_id, item_id, quantity, status) VALUES (%s, %s, %s,'pending')",
            (order.user_id, order.item_id, order.quantity)
        )
        conn.commit()
    
    conn.close()
    return {"message": "Order placed successfully"}


@router.patch("/{order_id}/status")
def update_order(order_id: int, auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    with conn.cursor() as cursor:
        cursor.execute("UPDATE orders SET status = 'completed' WHERE id = %s", (order_id,))
        conn.commit()
    
    conn.close()
    return {"message": "Order updated successfully"}