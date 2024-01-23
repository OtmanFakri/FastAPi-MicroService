from fastapi import FastAPI
from dotenv import load_dotenv
from redis_om import get_redis_connection, HashModel
import os

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)
# Load environment variables from .env file
load_dotenv()

# Get Redis configuration from environment variables
redis_host = os.getenv("REDIS_HOST")
redis_port = int(os.getenv("REDIS_PORT"))
redis_password = os.getenv("REDIS_PASSWORD")

# This should be a different database
redis = get_redis_connection(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/")
async def root():
    return {"message": "Hello in the microservice : Product"}

@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)
    if product:
        return {
            'id': product.pk,
            'name': product.name,
            'price': product.price,
            'quantity': product.quantity
        }
    else:
        # Handle the case where the product is not found
        return {"error": "Product not found"}

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.post('/products')
def create(product_data: dict):
    product = Product(**product_data)
    return product.save()

@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)