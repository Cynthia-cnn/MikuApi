# Routing

## GET

@app.get("/")
def home():
    return {"msg": "hello"}

## POST

@app.post("/login")
def login(username: str):
    return {"user": username}

## Path Params

@app.get("/user/{id}")
def get_user(id: int):
    return {"id": id}
