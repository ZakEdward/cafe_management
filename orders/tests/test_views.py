import pytest
from django.urls import reverse
from orders.models import Order

@pytest.mark.django_db
def test_order_list_view(client):
    """
    Тест отображения списка заказов.
    """
    order = Order.objects.create(
        table_number=5,
        items=[{"name": "Борщ", "price": 150}],
        status="pending"
    )
    response = client.get(reverse('order_list'))
    assert response.status_code == 200
    assert order.table_number in [o.table_number for o in response.context['orders']]

@pytest.mark.django_db
def test_add_order_view(client):
    """
    Тест добавления нового заказа.
    """
    data = {
        'table_number': 10,
        'items': '[{"name": "Чай", "price": 50}]',
        'status': 'pending'
    }
    response = client.post(reverse('add_order'), data)
    assert response.status_code == 302  # Перенаправление после успешного добавления
    assert Order.objects.count() == 1
    assert Order.objects.first().total_price == 50

@pytest.mark.django_db
def test_delete_order_view(client):
    """
    Тест удаления заказа.
    """
    order = Order.objects.create(
        table_number=5,
        items=[{"name": "Борщ", "price": 150}],
        status="pending"
    )
    response = client.post(reverse('delete_order', args=[order.id]))
    assert response.status_code == 302  # Перенаправление после удаления
    assert Order.objects.count() == 0