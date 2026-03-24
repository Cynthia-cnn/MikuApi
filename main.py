# main.py

from mikuapi import MikuAPI, Depends
from mikuapi.middleware.error_handler import ErrorMiddleware
from mikuapi.middleware.cors import CORSMiddleware
from mikuapi.security.jwt import encode
from mikuapi.security.auth import require_user
from mikuapi.limiter import limit


app = MikuAPI()

# Middleware
app.add_middleware(ErrorMiddleware)
app.add_middleware(CORSMiddleware)


# Root
@app.get("/")
def home():
    return {
        "name": "MikuAPI",
        "status": "running"
    }


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Login (JWT)
@app.post("/login")
def login(username: str):
    token = encode({"user": username})
    return {"token": token}


# Protected route
@app.get("/me")
def me(user=Depends(require_user)):
    return user


# Rate limited endpoint
@app.get("/limited")
@limit(3, window=5)
def limited():
    return {"msg": "rate limit active"}


# Example with params
@app.get("/user/{id}")
def get_user(id: int):
    return {
        "user_id": id
    }