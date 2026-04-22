import pandas as pd
import random

products = []

brands = ["Nike", "Adidas", "Puma", "Reebok"]

descriptions_map = {
    "Nike": [
        "Nike running shoes for athletes",
        "Nike sports shoes for high performance",
        "Nike lightweight training shoes"
    ],
    "Adidas": [
        "Adidas stylish sneakers for casual wear",
        "Adidas comfortable street shoes",
        "Adidas ultraboost running shoes"
    ],
    "Puma": [
        "Puma training shoes for gym",
        "Puma sports shoes for daily use",
        "Puma lightweight running shoes"
    ],
    "Reebok": [
        "Reebok fitness shoes for workouts",
        "Reebok gym training sneakers",
        "Reebok durable running shoes"
    ]
}

for i in range(1000):
    brand = random.choice(brands)

    products.append({
        "id": i,   # 🔥 IMPORTANT (for future DB)
        "name": f"{brand} Shoes {i}",
        "description": random.choice(descriptions_map[brand]),
        "brand": brand,
        "price": random.randint(500, 5000),
        "rating": round(random.uniform(1, 5), 1),
        "category": "shoes"
    })

df = pd.DataFrame(products)

df.to_csv("backend/data/products.csv", index=False)

print("CSV created successfully!")