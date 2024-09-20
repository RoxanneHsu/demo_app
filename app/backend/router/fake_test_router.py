import random
from faker import Faker
from fastapi import APIRouter, HTTPException
from controller.order_controller import OrderController
from models.order_model import OrderRequestModel
import logging
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(tags=["Test Tool"])
order_controller = OrderController("test_db")
faker = Faker()

@router.post("/generate_fake_orders/")
def create_fake_orders():
    """創建十筆假訂單"""
    try:
        order_controller.create_order_table()
        fake_orders = []

        for _ in range(10):
            brands = ["apple", "aws", "google", "meta"]

            # 隨機生成 weight 和 capacity
            weight = round(random.uniform(0, 10.0), 2)  # weight 介於 0 到 10.0 之間
            capacity = round(random.uniform(300.0, 900.0), 2)  # capacity 介於 300 到 900 之間

            # 使用 Faker 生成假訂單數據
            order_request = OrderRequestModel(
                brand=random.choice(brands),
                product=faker.word(),
                weight=weight,
                capacity=capacity
            )
            fake_orders.append(order_request.model_dump())

        result = order_controller.insert_order(fake_orders)

        if fake_orders:
            return {"status": "Success", "fake_orders": fake_orders}

        raise HTTPException(status_code=400, detail="Order creation failed")
    except SQLAlchemyError as e:
        logging.error(f"Error generating fake orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
