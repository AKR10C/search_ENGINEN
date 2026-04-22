from fastapi import FastAPI
from search import search_products

app = FastAPI()

@app.get("/")
def home():
    return {'message':"API working"}

@app.get("/search")
def search(q: str):
    result = search_products(q)
    return {"result": result}

