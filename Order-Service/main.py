import time

from fastapi import FastAPI
from dotenv import load_dotenv
from redis_om import get_redis_connection, HashModel
import os
from starlette.requests import Request
from fastapi.background import BackgroundTasks
import requests
from starlette.middleware.cors import CORSMiddleware
from get_temperatures_by_id import temperatures_from_dict

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

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis



@app.get("/")
async def root():
    return {"message": "Hello in the microservice : Order"}

@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)

@app.get('/orders')
def get():
    return Order.all_pks()





@app.post('/orders')
async def create(request: Request,background_tasks: BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    if req.status_code == 200:
            product_data = req.json()
            req_prod= temperatures_from_dict(product_data)
            order = Order(
                product_id=body['id'],
                price=req_prod.price,
                fee=0.2 * req_prod.price,
                total=1.2 * req_prod.price,
                quantity=body['quantity'],
                status='pending'
            )
            order.save()
            background_tasks.add_task(order_completed, order)
            return order

    else:
        # Handle the case when the request was not successful
        print(f"Failed to fetch product with ID {request}. Status code: {req.status_code}")
        return None

def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
