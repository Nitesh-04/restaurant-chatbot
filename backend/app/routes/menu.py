from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter()

@router.get("/")
def get_menu():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM menu")
        menu_items = cursor.fetchall()
    
    conn.close()
    return {"menu": menu_items}
