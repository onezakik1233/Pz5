import pytest
import os
import pyodbc
from orders_service.app import app

# Переменные среды для теста
DB_SERVER = os.getenv('DB_SERVER', 'localhost')
DB_DATABASE = os.getenv('DB_DATABASE', 'MicroshopOrders')
DB_USER = os.getenv('DB_USER', 'sa')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'TestPass123!')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_db():
    """Очистка БД перед тестом"""
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USER};PWD={DB_PASSWORD};TrustServerCertificate=yes;'
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Orders")
        conn.commit()
        conn.close()
    except Exception:
        pass

def test_create_order(client):
    # Тест: Создание заказа
    resp = client.post('/orders', json={"product_id": 1, "customer_id": 1, "quantity": 10})
    assert resp.status_code == 201
    assert resp.json['id'] > 0