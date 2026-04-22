import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import numpy as np
from db import get_products_by_ids
import os 
import re



csv_path = os.path.join(os.path.dirname(__file__), "data/products.csv")
df = pd.read_csv(csv_path)


df["text"] = (
    df["name"] + " " +
    df["brand"] + " " +
    df["description"] + " " +
    df["category"]
)

df["text"] = df["text"].str.lower()

df["text"] = df["text"].str.lower()

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["text"])

# Tokenize text
tokenized_corpus = [doc.split(" ") for doc in df["text"]]

# Create BM25 model
bm25 = BM25Okapi(tokenized_corpus)

def extract_rating(query):
    match = re.search(r'rating above (\d+)', query)
    if match:
        return float(match.group(1))
    return None


def extract_price(query):
    match = re.search(r'under (\d+)', query)
    if match:
        return int(match.group(1))
    return None
#feature filtering 
def extract_sort(query):
    if "low price" in query:
        return ("price", "asc")
    elif "high price" in query:
        return ("price", "desc")
    elif "high rating" in query:
        return ("rating", "desc")
    return None

def search_products(query):
    print("DEBUG: BM25 + MySQL running")
    query = query.lower()
    tokenized_query = query.split()

    scores = bm25.get_scores(tokenized_query)

    results_df = df.copy()
    results_df["score"] = scores

    top_results = results_df.sort_values(by="score", ascending=False).head(10)

    top_ids = top_results["id"].tolist()

    sort_option = extract_sort(query)

    # 🔥 USE FUNCTION HERE
    max_price = extract_price(query)
    min_rating = extract_rating(query)

    final_results = get_products_by_ids(top_ids, max_price, min_rating,sort_option)

    return final_results[:5]