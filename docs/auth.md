# Authentication

from mikuapi.security.jwt import encode

@app.post("/login")
def login(username: str):
    return {"token": encode({"user": username})}

from mikuapi.security.auth import require_user
from mikuapi import Depends

@app.get("/me")
def me(user = Depends(require_user)):
    return user
