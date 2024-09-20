import logging
import traceback
from sqlalchemy import engine_from_config, text
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

class Database:
    _base_sqlalchemy_settings = {
            "sqlalchemy.pool_size": 5,
            "sqlalchemy.max_overflow": 2,
            "sqlalchemy.pool_timeout": 30,
            "sqlalchemy.pool_recycle": 1800,
            "sqlalchemy.echo": False,
        }
    _db_names = [
        'test_db'
        ]

    def __init__(self, db_name: str):
        if db_name not in self._db_names:
            raise ValueError(f"Invalid database name: {db_name}")

        self.db_name = db_name
        self.config = {
            self.db_name: self._create_sqlalchemy_config(db_name),
        }
    
    def _create_sqlalchemy_config(self, db_name: str) -> dict:
        load_dotenv()
        db_host = os.getenv('MYSQL_HOST')
        db_port = os.getenv('MYSQL_PORT')
        db_user = os.getenv('MYSQL_USER')
        db_password = os.getenv('MYSQL_PASSWORD')
        url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        
        return {
            "sqlalchemy.url": url,
            **self._base_sqlalchemy_settings,
        }

    def _open_connection(self):
        try:
            conn = engine_from_config(self.config[self.db_name], future=True).connect()
            logging.info(f"Connected to database: {self.db_name}")
            return conn
        except SQLAlchemyError as e:
            logging.error(f"Failed to connect to database {self.db_name}: {str(e)}")
            return None  

    def __enter__(self):
        self.conn = self._open_connection()
        if self.conn:
            logging.info(f"{self.db_name} db connection opened")
        else:
            logging.error(f"Failed to open {self.db_name} db connection")
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            logging.info(f"{self.db_name} db connection closed")
            self.conn.close()

class SQLExecutor:
    def __init__(self, db_name: str = None, conn=None):
        if conn:
            self.conn = conn
        else:
            self.database = Database(db_name)
            self.conn = self.database.__enter__()

    def _execute(self, sql: str, data: list = None):
        if not self.conn:
            logging.error("Database connection is not established.")
            raise ConnectionError("No database connection established.")
        try:
            if data:
                result = self.conn.execute(text(sql), data)
            else:
                result = self.conn.execute(text(sql))
            self.conn.commit()
            logging.info(f"SQL executed successfully: {sql}")
            return result
        except SQLAlchemyError as e:
            self.conn.rollback()
            logging.error(f"Failed to execute SQL: {sql}, Error: {str(e)}")
            logging.error(traceback.format_exc())
            return None
        except Exception as e:
            self.conn.rollback()
            logging.error(f"Unexpected error during SQL execution: {sql}")
            logging.error(traceback.format_exc())
            return None

    def execute_query(self, sql: str):
        try:
            result = self.conn.execute(text(sql))
            return result
        except SQLAlchemyError as e:
            logging.error(f"SQL Execution failed: {e}")
            return None
        
    def execute_many(self, sql: str, insert_data: list):
        return self._execute(sql, insert_data)