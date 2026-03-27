# Getting Started

## Install

pip install mikuapi

## Create App

from mikuapi import MikuAPI

app = MikuAPI()

@app.get("/")
def home():
    return {"msg": "Hello"}

## Run

mikuapi run main:app --reload
