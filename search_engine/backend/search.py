import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from rank_bm25 import BM25Okapi
import numpy as np
from backend.db import get_products_by_ids
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

    # Extract filters from query FIRST
    max_price = extract_price(query)
    min_rating = extract_rating(query)
    sort_option = extract_sort(query)

    # Filter the dataframe by price and rating BEFORE ranking
    filtered_df = df.copy()
    
    # Handle NaN values
    filtered_df = filtered_df.dropna(subset=["price", "rating", "text"])
    
    if max_price:
        filtered_df = filtered_df[filtered_df["price"] <= max_price]
    if min_rating:
        filtered_df = filtered_df[filtered_df["rating"] >= min_rating]

    # Calculate BM25 scores only on filtered results
    if len(filtered_df) == 0:
        return []  # No results match the filters

    # Reset index to prevent index misalignment
    filtered_df = filtered_df.reset_index(drop=True)

    # Recalculate BM25 for filtered dataset
    filtered_text = filtered_df["text"].tolist()
    tokenized_corpus_filtered = [doc.split(" ") for doc in filtered_text]
    bm25_filtered = BM25Okapi(tokenized_corpus_filtered)
    scores = bm25_filtered.get_scores(tokenized_query)

    # Add scores to filtered dataframe
    filtered_df["score"] = scores

    # Sort by relevance (BM25 score) - PRIMARY ranking
    top_results = filtered_df.sort_values(by="score", ascending=False).head(10)

    # Apply secondary sort if requested (price/rating sorting)
    if sort_option:
        column, order = sort_option
        top_results = top_results.sort_values(by=column, ascending=(order.lower() == "asc"))

    top_ids = top_results["id"].tolist()

    # Get final results from database (without applying filters again)
    # final_results = get_products_by_ids(top_ids, max_price=None, min_rating=None, sort_option=None)
    return top_results.head(5)[["id", "name", "price", "rating"]].to_dict(orient="records")
    # return final_results[:5]