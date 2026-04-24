from fastapi import FastAPI,Query   
from backend.search import search_products
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {'message':"API working"}

# @app.get("/search")
# def search(q: str):
#     if not q or len(q.strip()) == 0:
#         return {"result": [], "error": "Query cannot be empty"}
#     try:
#         result = search_products(q)
#         return {"result": result}
#     except Exception as e:
#         return {"result": [], "error": str(e)}

@app.get("/search")
def search(
    q: str,
    maxPrice: int = None,
    minRating: float = None,
    sort: str = None
):
    return {
        "result": search_products(q, maxPrice, minRating, sort)
    }
