import pytest
from rest_framework.test import APIClient
from orders.models import Order

@pytest.mark.django_db
def test_api_order_list():
    """
    Тест получения списка заказов через API.
    """
    client = APIClient()
    order = Order.objects.create(
        table_number=5,
        items=[{"name": "Борщ", "price": 150}],
        status="pending"
    )
    response = client.get('/api/orders/')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['table_number'] == 5

@pytest.mark.django_db
def test_api_create_order():
    """
    Тест создания заказа через API.
    """
    client = APIClient()
    data = {
        'table_number': 10,
        'items': [{"name": "Чай", "price": 50}],
        'status': 'pending'
    }
    response = client.post('/api/orders/', data, format='json')
    assert response.status_code == 201  # Успешное создание
    assert Order.objects.count() == 1
    assert Order.objects.first().total_price == 50

@pytest.mark.django_db
def test_api_update_order():
    """
    Тест обновления заказа через API.
    """
    client = APIClient()
    order = Order.objects.create(
        table_number=5,
        items=[{"name": "Борщ", "price": 150}],
        status="pending"
    )
    data = {
        'status': 'ready'
    }
    response = client.patch(f'/api/orders/{order.id}/', data, format='json')
    assert response.status_code == 200
    assert Order.objects.first().status == 'ready'

@pytest.mark.django_db
def test_api_delete_order():
    """
    Тест удаления заказа через API.
    """
    client = APIClient()
    order = Order.objects.create(
        table_number=5,
        items=[{"name": "Борщ", "price": 150}],
        status="pending"
    )
    response = client.delete(f'/api/orders/{order.id}/')
    assert response.status_code == 204  # Успешное удаление
    assert Order.objects.count() == 0