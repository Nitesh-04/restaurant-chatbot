from fastapi import APIRouter,Depends,HTTPException
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
    
    try:
        with conn.cursor() as cursor:
            # Get order details
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return {"error": "Order not found"}
            
            # Get all items for the order
            cursor.execute(
                "SELECT item_id, quantity FROM order_items WHERE order_id = %s",
                (order_id,)
            )
            items = cursor.fetchall()
        
        return {"order": order, "items": items}
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        conn.close()


class OrderCreate(BaseModel):
    user_id: int
    item_id: int
    quantity: int


@router.post("/")
def place_order(user_id: int):

    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    with conn.cursor() as cursor:
        # Check if the cart is empty
        cursor.execute("SELECT * FROM cart WHERE user_id = %s", (user_id,))
        cart_items = cursor.fetchall()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        # Create a new order
        cursor.execute("INSERT INTO orders (user_id, status) VALUES (%s, 'pending')", (user_id,))
        order_id = cursor.lastrowid

        # Move items from cart to order_items
        for item in cart_items:
            cursor.execute(
                "INSERT INTO order_items (order_id, item_id, quantity) VALUES (%s, %s, %s)",
                (order_id, item["item_id"], item["quantity"])
            )

        # Clear the cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        conn.commit()
    
    conn.close()
    return {"message": "Order placed successfully", "order_id": order_id}



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