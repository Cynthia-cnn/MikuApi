# MikuAPI

Fast. Simple. Built from scratch.

MikuAPI is a lightweight ASGI web framework designed for simplicity and performance.



## Features

- Fast routing
- Dependency Injection
- JWT Authentication
- Rate limiting
- Middleware support
- CLI



## Quick Start

from mikuapi import MikuAPI

app = MikuAPI()

@app.get("/")
def home():
    return {"message": "Hello from MikuAPI"}

Run:

mikuapi run main:app --reload



## Why MikuAPI?

- Easy to understand
- Built from scratch
- Lightweight
- Fast



## Next

See other sections for more details.
