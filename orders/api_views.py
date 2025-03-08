from rest_framework import generics, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    """
    Представление для получения списка заказов или создания нового заказа.

    Методы:
    - GET: Возвращает список всех заказов.
    - POST: Создает новый заказ.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Представление для работы с конкретным заказом.

    Методы:
    - GET: Возвращает информацию о заказе.
    - PUT/PATCH: Обновляет информацию о заказе.
    - DELETE: Удаляет заказ.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_update(self, serializer):
        # Автоматический расчет total_price при обновлении
        instance = serializer.save()
        instance.total_price = instance.calculate_total_price()
        instance.save()