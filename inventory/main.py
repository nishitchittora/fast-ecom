import os

from fastapi import FastAPI, status, Request
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
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


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


class ProductData(BaseModel):
    name: str
    price: float
    quantity: int


class ProductsData(List[ProductData]):
    pass


@app.get("/products", status_code=status.HTTP_200_OK, response_model=ProductsData)
def all_products():
    # return ProductData(data=[Product.get(pk).dict() for pk in Product.all_pks()], many=True).data
    return [format(pk) for pk in Product.all_pks()]


def format(pk: int):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


@app.post("/products")
def create_product(product: Product):
    return product.save()


@app.get("/products/{pk}")
def get_product(pk: int):
    return Product.get(pk)


@app.delete("/products/{pk}")
def delete_product(pk: int):
    return Product.delete(pk)
