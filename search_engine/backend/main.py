from fastapi import FastAPI
from search import search_products
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("API_CORS_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {'message':"API working"}

@app.get("/search")
def search(q: str):
    if not q or len(q.strip()) == 0:
        return {"result": [], "error": "Query cannot be empty"}
    try:
        result = search_products(q)
        return {"result": result}
    except Exception as e:
        return {"result": [], "error": str(e)}

