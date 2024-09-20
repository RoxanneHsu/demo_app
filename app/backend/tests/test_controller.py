from controller.order_controller import OrderController
from unittest.mock import MagicMock

def test_insert_order():
    controller = OrderController("test_db")
    controller.executor = MagicMock()
    
    order_data = {
        "brand": "test_brand",
        "product": "test_product",
        "weight": 1.0,
        "capacity": 100.0
    }
    controller.insert_order([order_data])
    controller.executor.execute_many.assert_called_once()

def test_update_order():
    controller = OrderController("test_db")
    controller.executor = MagicMock()
    
    controller.update_order("test_brand", "new_product")
    controller.executor.execute_many.assert_called_once()

def test_delete_order():
    controller = OrderController("test_db")
    controller.executor = MagicMock()
    
    controller.delete_order("test_brand")
    controller.executor.execute_many.assert_called_once()

def test_get_orders():
    controller = OrderController("test_db")
    controller.executor = MagicMock()
    controller.executor.execute_query.return_value.fetchall.return_value = [
        {"brand": "test_brand", "product": "test_product", "weight": 1.0, "capacity": 100.0}
    ]
    
    orders = controller.get_orders()
    assert len(orders) > 0
    assert orders[0]["brand"] == "test_brand"
