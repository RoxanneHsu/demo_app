import logging
from database.database import SQLExecutor
from sqlalchemy.exc import SQLAlchemyError

class OrderController:
    def __init__(self, db_name: str):
        self.executor = SQLExecutor(db_name)

    def create_order_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(255),
            product VARCHAR(255),
            weight Float,
            capacity Float
        );
        '''
        try:
            self.executor.execute_query(create_table_query)
            logging.info("Order table created successfully.")
        except SQLAlchemyError as e:
            logging.error(f"Error creating order table: {str(e)}")
            raise

    def insert_order(self, orders: list):
        """使用 Pydantic 模型建立新訂單"""
        insert_query = '''
        INSERT INTO orders (brand, product, weight, capacity)
        VALUES (:brand, :product, :weight, :capacity);
        '''
        try:
            result = self.executor.execute_many(insert_query, orders)
            logging.info(f"{result.rowcount} orders inserted successfully.")
            return result.rowcount
        except SQLAlchemyError as e:
            logging.error(f"Error inserting orders: {str(e)}")
            raise

    def get_orders(self):
        select_query = 'SELECT id, brand, product, weight, capacity FROM orders;'
        try:
            result = self.executor.execute_query(select_query)
            orders = result.fetchall() if result else []
            logging.info(f"Fetched {len(orders)} orders.")
            return orders
        except SQLAlchemyError as e:
            logging.error(f"Error fetching orders: {str(e)}")
            raise

    def update_order(self, brand, product):
        update_query = '''
        UPDATE orders SET product = :product WHERE brand = :brand;
        '''
        try:
            result = self.executor.execute_many(update_query, [{
                'brand': brand,
                'product': product
            }])
            logging.info(f"Order updated for brand {brand}.")
        except SQLAlchemyError as e:
            logging.error(f"Error updating order for brand {brand}: {str(e)}")
            raise

    def delete_order(self, brand):
        delete_query = 'DELETE FROM orders WHERE brand = :brand;'
        try:
            self.executor.execute_many(delete_query, [{'brand': brand}])
            logging.info(f"Order deleted for brand {brand}.")
        except SQLAlchemyError as e:
            logging.error(f"Error deleting order for brand {brand}: {str(e)}")
            raise
