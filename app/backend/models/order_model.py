from pydantic import BaseModel, confloat

class Order(BaseModel):
    id: int
    brand: str
    product: str
    weight: confloat(ge=0) 
    capacity: confloat(ge=0) 


class OrderRequestModel(BaseModel):
    brand: str
    product: str
    weight: confloat(ge=0) 
    capacity: confloat(ge=0) 


class ResponseModel(BaseModel):
    id: int
    request_model: OrderRequestModel




