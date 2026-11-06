import requests
import pandas as pd
import random
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient

# Azure connection configuration
CONNECTION_STRING = ""# Copy from Azure acces keys
CONTAINER_NAME = "data"
BLOB_NAME = "real_ecommerce_orders.csv"

print("📥 Fetching products and users structure from API...")
users_res = requests.get("https://fakestoreapi.com/users").json()
products_res = requests.get("https://fakestoreapi.com/products").json()

# Prepare base users data
users_list = []
for u in users_res:
    users_list.append({
        'userId': u['id'],
        'CustomerName': f"{u['name']['firstname'].capitalize()} {u['name']['lastname'].capitalize()}",
        'City': u['address']['city'].capitalize()
    })
users_df = pd.DataFrame(users_list)

# Prepare base products data
products_list = []
for p in products_res:
    products_list.append({
        'ProductId': p['id'],
        'price': p['price'],
        'category': p['category']
    })
products_df = pd.DataFrame(products_list)

print("⚙️ Generating 2,000 transaction records...")
np_orders = []
start_date = datetime.now() - timedelta(days=180)

for i in range(1, 2001):
    random_user = users_df.sample(n=1).iloc[0]
    random_prod = products_df.sample(n=1).iloc[0]
    
    order_date = start_date + timedelta(days=random.randint(0, 180))
    quantity = random.randint(1, 5)
    
    np_orders.append({
        'CartId': 5000 + (i % 400),
        'userId': random_user['userId'],
        'CustomerName': random_user['CustomerName'],
        'City': random_user['City'],
        'OrderDate': order_date.strftime('%Y-%m-%d'),
        'ProductId': random_prod['ProductId'],
        'Category': random_prod['category'],
        'Quantity': quantity,
        'UnitPrice': random_prod['price'],
        'TotalPrice': round(quantity * random_prod['price'], 2)
    })

final_df = pd.DataFrame(np_orders)

local_file = "ecommerce_large_orders.csv"
final_df.to_csv(local_file, index=False)
print(f"✅ Generated and processed {len(final_df)} records!")

# Uploading data to Azure Blob Storage
try:
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=BLOB_NAME)

    with open(local_file, "rb") as data_file:
        blob_client.upload_blob(data_file, overwrite=True)
    
    print(f"🚀 2,000 records successfully uploaded to Azure Blob Storage (`{CONTAINER_NAME}/{BLOB_NAME}`)!")
except Exception as e:
    print(f"❌ Error uploading to Azure: {e}")