import random
from faker import Faker
from fastapi import APIRouter, HTTPException, Body
from typing import List
from controller.order_controller import OrderController
from models.order_model import OrderRequestModel, Order
import logging
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(tags=["Order Management"])
order_controller = OrderController("test_db")
faker = Faker()

@router.post("/create_order")
def create_new_order(orders: List[OrderRequestModel] = Body(...)):
    """創建新訂單"""
    try:
        order_controller.create_order_table()
        result = order_controller.insert_order(orders=[order.model_dump() for order in orders])
        if result:
            return result
        raise HTTPException(status_code=400, detail="Order creation failed")
    except SQLAlchemyError as e:
        logging.error(f"Error creating new order: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/read_orders", response_model=list[Order])
def read_orders():
    """讀取所有訂單"""
    try:
        orders = order_controller.get_orders()
        return orders
    except SQLAlchemyError as e:
        logging.error(f"Error reading orders: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/update_order")
def modify_order(brand: str, product: str):
    """修改指定訂單"""
    try:
        order_controller.update_order(brand, product)
        return {"status": "Order updated"}
    except SQLAlchemyError as e:
        logging.error(f"Error updating order for brand {brand}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/delete_order")
def remove_order(brand: str):
    """刪除指定訂單"""
    try:
        order_controller.delete_order(brand)
        return {"status": "Order deleted"}
    except SQLAlchemyError as e:
        logging.error(f"Error deleting order for brand {brand}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")