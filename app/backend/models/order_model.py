from pydantic import BaseModel

class Order(BaseModel):
    id: int
    brand: str
    product: str
    weight: float
    capacity: float


class OrderRequestModel(BaseModel):
    brand: str
    product: str
    weight: float
    capacity: float


class ResponseModel(BaseModel):
    id: int
    request_model: OrderRequestModel




