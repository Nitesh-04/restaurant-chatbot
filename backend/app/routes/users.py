from fastapi import APIRouter, Depends
from app.database import get_db_connection
from app.auth import require_admin

router = APIRouter()

@router.get("/")
def get_users(auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
    
    conn.close()
    return {"users": users}


@router.get("/{user_id}")
def get_user(user_id: int, auth: bool = Depends(require_admin)):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    
    conn.close()
    
    if not user:
        return {"error": "User not found"}
    
    return {"user": user}
