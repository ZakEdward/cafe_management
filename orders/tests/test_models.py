import pytest
from django.core.exceptions import ValidationError
from orders.models import Order

@pytest.mark.django_db
def test_order_creation():
    """
    Тест создания заказа.
    """
    order = Order.objects.create(
        table_number=5,
        items=[{"name": "Борщ", "price": 150}, {"name": "Чай", "price": 50}],
        status="pending"
    )
    assert order.table_number == 5
    assert order.total_price == 200
    assert order.status == "pending"

@pytest.mark.django_db
def test_invalid_items():
    """
    Тест валидации некорректных данных в поле items.
    """
    order = Order(
        table_number=1,
        items="invalid_data",  # Некорректный формат
        status="pending"
    )
    with pytest.raises(ValidationError) as excinfo:
        order.full_clean()  # Вызывает валидацию модели
    assert 'Список блюд должен быть в формате JSON.' in str(excinfo.value)