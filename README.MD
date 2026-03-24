# MikuAPI

A lightweight Python web framework built from scratch.

## Install

pip install mikuapi

## Quick Start

from mikuapi import MikuAPI

app = MikuAPI()

@app.get("/")
def home():
    return {"message": "Hello from MikuAPI"}

Run server:

mikuapi run main:app --reload

## Documentation

Full documentation coming soon.

## License

MIT