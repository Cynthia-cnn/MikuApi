# Dependency Injection

from mikuapi import Depends

def get_user():
    return {"name": "miku"}

@app.get("/me")
def me(user = Depends(get_user)):
    return user
