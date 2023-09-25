from pydantic import BaseModel
from datetime import datetime


class Address(BaseModel):
    city : str
    country : str
    zip_code : str

class Items(BaseModel):
    product_id : str
    product_quantity : int

class Order(BaseModel):
    time_stamp : datetime = datetime.now()
    items : Items
    total_amount : int
    address : Address