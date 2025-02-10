from fastapi import APIRouter,Depends,HTTPException
from app.database import get_db_connection
from app.auth import require_admin

router = APIRouter()

@router.get("/{order_id}")
def track_order(order_id: int, auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    try:
        with conn.cursor() as cursor:
            # Get order details
            cursor.execute("SELECT status FROM orders WHERE id = %s", (order_id,))
            status = cursor.fetchone()
            
            if not status:
                return {"error": "Order not found"}
            
        return status
    
    except Exception as e:
        return {"error": str(e)}
    
    finally:
        conn.close()