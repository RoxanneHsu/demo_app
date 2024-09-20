import streamlit as st
import requests

# 設置 FastAPI 的後端 API 端點
API_BASE_URL = "http://api:8000"

st.title("訂單管理系統")
# 功能 1: 建立假訂單
st.header("建立假訂單")
if st.button("建立假訂單"):
    try:
        response = requests.post(f"{API_BASE_URL}/fake/generate_fake_orders/")
        if response.status_code == 200:
            fake_orders = response.json()
            st.write("訂單列表：")
            st.dataframe(fake_orders["fake_orders"])
        else:
            st.error("無法建立假訂單")
    except Exception as e:
        st.error(f"發生錯誤: {e}")

# 功能 2: 顯示所有訂單
st.header("查看所有訂單")
if st.button("顯示訂單"):
    try:
        response = requests.get(f"{API_BASE_URL}/db_crud/read_orders")
        if response.status_code == 200:
            orders = response.json()
            st.write("訂單列表：")
            st.dataframe(orders)
        else:
            st.error("無法獲取訂單資料")
    except Exception as e:
        st.error(f"發生錯誤: {e}")

# 功能 3: 創建新訂單
st.header("創建新訂單")
with st.form(key='create_order_form'):
    brand = st.text_input("品牌")
    product = st.text_input("產品名稱")
    weight = st.number_input("重量", min_value=0.0, step=0.1)
    capacity = st.number_input("容量", min_value=0.0, step=0.1)
    
    submit_button = st.form_submit_button(label="創建訂單")

if submit_button:
    new_order = {
        "brand": brand,
        "product": product,
        "weight": weight,
        "capacity": capacity
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/db_crud/create_order", json=[new_order])
        if response.status_code == 200:
            st.success("訂單創建成功!")
        else:
            st.error(f"訂單創建失敗: {response.text}")
    except Exception as e:
        st.error(f"發生錯誤: {e}")

# 功能 4: 修改訂單
st.header("修改訂單")
with st.form(key='modify_order_form'):
    brand_to_modify = st.text_input("要修改的品牌")
    new_product = st.text_input("新產品名稱")
    submit_modify_button = st.form_submit_button(label="修改訂單")

if submit_modify_button:
    try:
        response = requests.put(f"{API_BASE_URL}/db_crud/update_order", params={"brand": brand_to_modify, "product": new_product})
        if response.status_code == 200:
            st.success("訂單修改成功!")
        else:
            st.error(f"訂單修改失敗: {response.text}")
    except Exception as e:
        st.error(f"發生錯誤: {e}")

# 功能 5: 刪除訂單
st.header("刪除訂單")
with st.form(key='delete_order_form'):
    brand_to_delete = st.text_input("要刪除的品牌")
    submit_delete_button = st.form_submit_button(label="刪除訂單")

if submit_delete_button:
    try:
        response = requests.delete(f"{API_BASE_URL}/db_crud/delete_order", params={"brand": brand_to_delete})
        if response.status_code == 200:
            st.success("訂單刪除成功!")
        else:
            st.error(f"訂單刪除失敗: {response.text}")
    except Exception as e:
        st.error(f"發生錯誤: {e}")
