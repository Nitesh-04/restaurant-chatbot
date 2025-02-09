from fastapi import FastAPI
from app.routes import users, orders, menu ,cart

app = FastAPI()


app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])

@app.get("/")
def root():
    return {"message": "Welcome to the Restaurant Chatbot API"}
