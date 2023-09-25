# API which gives data about list of products.


from fastapi import FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
from bson import ObjectId, json_util
from mongo_db_conn import MongoConnection
from userModels import Order

app = FastAPI()

#This api gives list of products available in the system rite now.
@app.get('/available_products')
def all_items():
    dbconn = MongoConnection()
    conn = dbconn.mongodbconn().get_collection('products')
    product_list = []
    data = conn.find({})
    for i in data:
        if i['quantity'] > 0:
            product_list.append(i['name'])
    return JSONResponse(content=({'products_available': product_list}))


#This api creates a new order
@app.post('/new_order')
def new_orders(O1:Order):
    dbconn = MongoConnection()
    conn = dbconn.mongodbconn().get_collection('orders')
    result = conn.insert_one(O1.model_dump())
    ack = result.acknowledged
    return {"insertion": ack}

#This api fetches all orders from order collections using pagination limit.
@app.get('/orders/{limit}')
def all_orders(limit:int):
    dbconn = MongoConnection()
    conn = dbconn.mongodbconn().get_collection('orders').find().limit(limit)
    stores = []
    for doc in conn:
        stores.append(doc)
    res = json.loads(json_util.dumps(stores))
    return JSONResponse(content=({'orders_list': res}))

#This api fetches all the details regarding an order by passing order id.
# we will be fetching order by via object id / order id
# params : order_id : _id : object_id
@app.get('/order_id/{order_id}')
def order_id(order_id:str):
    dbconn = MongoConnection()
    conn = dbconn.mongodbconn().get_collection('orders')
    object_id = ObjectId(order_id)
    order1 = conn.find_one({"_id":ObjectId("{0}".format(order_id))})
    return json.loads(json_util.dumps(order1))

# This API to update a product quantity.
@app.patch('/update')
def update_product(product : str, update_qty: int):
    dbconn = MongoConnection()
    conn = dbconn.mongodbconn().get_collection('products')
    existing_quantity = conn.find_one({"name":product})
    existing_quantity = json.loads(json_util.dumps(existing_quantity))['quantity']
    update_quantity = conn.update_one({"name" : product}, {"$set": { "quantity": existing_quantity + (update_qty)}})
    return json.loads(json_util.dumps(conn.find_one({"name":product}))) 

