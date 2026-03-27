from mikuapi import MikuAPI, Depends
from mikuapi.middleware.error_handler import ErrorMiddleware
from mikuapi.middleware.cors import CORSMiddleware
from mikuapi.security.jwt import encode
from mikuapi.security.auth import require_user
from mikuapi.limiter import limit
from mikuapi.schema import BaseModel


app = MikuAPI()

app.add_middleware(ErrorMiddleware)
app.add_middleware(CORSMiddleware)


@app.get("/")
def home():
    return {"name": "MikuAPI", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/login")
def login(username: str):
    token = encode({"user": username})
    return {"token": token}


@app.get("/me")
def me(user=Depends(require_user)):
    return user


@app.get("/limited")
@limit(3, window=5)
def limited():
    return {"msg": "rate limit active"}


@app.get("/user/{id}")
def get_user(id: int):
    return {"user_id": id}


class User(BaseModel):
    name: str
    age: int
    active: bool = True


@app.post("/users")
def create_user(user: User):
    return user


@app.get("/search")
def search(q: str, page: int = 1, tags: list = []):
    return {"query": q, "page": page, "tags": tags}


@app.post("/raw")
def raw(data: dict):
    return data


@app.post("/mix/{id}")
def mix(id: int, q: str, user: User):
    return {"id": id, "query": q, "user": user.dict()}


@app.get("/model")
def model():
    return User(name="miku", age=17)