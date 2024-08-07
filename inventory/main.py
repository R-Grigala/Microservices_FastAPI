from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-19093.c293.eu-central-1-1.ec2.redns.redis-cloud.com",
    port=19093,
    password="P3tALTScqGJ9QUH97cLv67G6tWSUAQ7B",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        'id' : product.pk,
        'name' : product.name,
        'price' : product.price,
        'quantity' : product.quantity
    }

@app.post('/products')
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk: str):
    try:
        return Product.get(pk)
    except KeyError:
        raise HTTPException(status_code=404, detail="Product not found")

@app.delete('/products/{pk}')
def delete(pk: str):
    try:
        product = Product.get(pk)
        product.delete(pk)
        return {"message": "Product deleted successfully", "id": pk}
    except KeyError:
        raise HTTPException(status_code=404, detail="Product not found")