import os
import time
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from typing import List
from pydantic import BaseModel
from starlette.requests import Request
from dotenv import load_dotenv
import requests
load_dotenv('../.env')

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:3000'],
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

redis = get_redis_connection(
    host=os.environ.get("REDIS_URL"),
    port=os.environ.get("REDIS_PORT"),
    password=os.environ.get("REDIS_PASSWORD"),
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis


@app.post("/orders")
async def create(request: Request, background_task=BackgroundTasks):
    body = await request.json()
    req = requests.get("http://localhost:8000/product/{}".format(body['id']))

    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2*product['price'],
        total=1.2*product['price'],
        quantity=body['quantity'],
        status="pending"
    )
    order.save()
    background_task.add_task(order_complete, order)
    return order


@app.get("/orders/{order_id}")
def orders(order_id: int):
    return Order.get(order_id)


def order_complete(order: Order):
    time.sleep(5)
    order.status = "complete"
    order.save()
