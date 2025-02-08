from fastapi import FastAPI
from app.routes import users, orders, menu  # Import your route files

app = FastAPI()

# Include the routers correctly
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])

@app.get("/")
def root():
    return {"message": "Welcome to the Restaurant Chatbot API"}
