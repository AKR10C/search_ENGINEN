from fastapi import FastAPI
from search import search_products
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {'message':"API working"}

@app.get("/search")
def search(q: str):
    result = search_products(q)
    return {"result": result}

