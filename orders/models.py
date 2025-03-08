from django.core.exceptions import ValidationError
from django.db import models

class Order(models.Model):
    """
    Модель для хранения информации о заказах в кафе.

    Поля:
    - table_number: Номер стола (целое число).
    - items: Список блюд в формате JSON (содержит название и цену каждого блюда).
    - total_price: Общая стоимость заказа (вычисляется автоматически).
    - status: Статус заказа ("в ожидании", "готово", "оплачено").
    - created_at: Дата и время создания заказа (автоматически генерируется).

    Методы:
    - calculate_total_price: Рассчитывает общую стоимость заказа.
    - save: Переопределяет метод сохранения для автоматического расчета total_price.
    """

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Список блюд", default=list)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая стоимость", default=0.0
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def calculate_total_price(self):
        """Рассчитывает общую стоимость заказа на основе списка блюд."""
        return sum(item['price'] for item in self.items)

    def save(self, *args, **kwargs):
        """Переопределяем метод save для автоматического расчета total_price."""
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def clean(self):
        """
        Валидация данных перед сохранением.
        """
        if not isinstance(self.items, list):
            raise ValidationError({'items': 'Список блюд должен быть в формате JSON.'})
        for item in self.items:
            if not isinstance(item, dict) or 'name' not in item or 'price' not in item:
                raise ValidationError({'items': 'Каждое блюдо должно содержать поля "name" и "price".'})

    def __str__(self):
        return f"Заказ #{self.id} (Стол {self.table_number})"