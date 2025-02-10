from fastapi import FastAPI
from app.routes import users, orders, menu ,cart, track, webhook

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(menu.router, prefix="/menu", tags=["Menu"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(track.router, prefix="/track", tags=["Track"])
app.include_router(webhook.router, prefix="/webhook", tags=["Webhook"])

@app.get("/")
def root():
    return {"message": "Welcome to the Restaurant Chatbot API"}
