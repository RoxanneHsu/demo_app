from models.order_model import OrderRequestModel
from pydantic import ValidationError
import pytest

def test_order_validation_success():
    """測試訂單模型的成功驗證"""
    data = {
        "brand": "valid_brand",
        "product": "valid_product",
        "weight": 1.0,
        "capacity": 500.0
    }
    order = OrderRequestModel(**data)
    assert order.brand == "valid_brand"
    assert order.product == "valid_product"
    assert order.weight == 1.0
    assert order.capacity == 500.0

def test_order_validation_failure_negative_weight():
    """測試訂單模型對重量為負值的驗證失敗"""
    data = {
        "brand": "valid_brand",
        "product": "valid_product",
        "weight": -1.0,  # 無效的重量
        "capacity": 500.0
    }
    with pytest.raises(ValidationError):
        OrderRequestModel(**data)

def test_order_validation_failure_missing_field():
    """測試訂單模型對缺失必要欄位的驗證失敗"""
    data = {
        "brand": "valid_brand",
        # 缺少 "product" 欄位
        "weight": 1.0,
        "capacity": 500.0
    }
    with pytest.raises(ValidationError):
        OrderRequestModel(**data)

def test_order_validation_failure_invalid_type():
    """測試訂單模型對無效類型的驗證失敗"""
    data = {
        "brand": "valid_brand",
        "product": "valid_product",
        "weight": "invalid_weight",  # 無效的類型
        "capacity": 500.0
    }
    with pytest.raises(ValidationError):
        OrderRequestModel(**data)
