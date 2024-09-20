from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_orders():
    response = client.get("/db_crud/read_orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_order():
    new_order = {
        "brand": "test_brand",
        "product": "test_product",
        "weight": 1.0,
        "capacity": 100.0
    }
    response = client.post("/db_crud/create_order", json=[new_order])
    assert response.status_code == 200

def test_modify_order():
    """測試修改訂單"""
    params = {
        "brand": "test_brand",
        "product": "modified_product"
    }
    response = client.put("/db_crud/update_order", params=params)
    assert response.status_code == 200
    assert response.json()["status"] == "Order updated"

def test_remove_order():
    """測試刪除訂單"""
    params = {
        "brand": "test_brand"
    }
    response = client.delete("/db_crud/delete_order", params=params)
    assert response.status_code == 200
    assert response.json()["status"] == "Order deleted"

def test_generate_fake_orders():
    """測試生成假訂單"""
    response = client.post("/fake/generate_fake_orders/")
    assert response.status_code == 200
    assert "fake_orders" in response.json()
    assert isinstance(response.json()["fake_orders"], list)
