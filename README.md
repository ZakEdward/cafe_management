# Управление заказами в кафе

## Описание
Приложение для управления заказами в кафе, написанное на Django. Позволяет добавлять, удалять, искать, изменять и 
отображать заказы через веб-интерфейс и REST API.

## Технологии
- Python 3.8+
- Django 4+
- Django REST Framework
- SQLite/PostgreSQL
- HTML/CSS

## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/cafe_management/cafe-management.git
2. Создайте виртуальное окружение:
   ```
   python3 -m venv venv
   source venv/bin/activate
3. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```   
4. Примените миграции:
   ```
   python manage.py migrate
   ```
5. Запустите сервер:
   ```
      python manage.py runserver
   ```
   
## Использование
Откройте браузер и перейдите по адресу http://127.0.0.1:8000/

# Веб-интерфейс
**Главная страница:** Список всех заказов.<br>
**Добавление заказа:** Форма для создания нового заказа.<br>
**Удаление заказа:** Удаление заказа по ID.<br>
**Поиск заказа:** Поиск по номеру стола или статусу.<br>
**Выручка за смену:** Расчет общей выручки за оплаченные заказы.<br>

## REST API
**GET /api/orders/:** Получить список всех заказов.<br>
**POST /api/orders/:** Создать новый заказ.<br>
<details>
    <summary>💡 Нажмите, чтобы увидеть пример запроса</summary>
    <pre><code class="json">
POST http://127.0.0.1:8000/api/orders/1/

Тело запроса:
{
    "table_number": 1,
    "items": [
        {
            "name": "Борщ",
            "price": 150
        },
        {
            "name": "Чай",
            "price": 50
        }
    ],
    "status": "pending"
}
    </code></pre>
</details>

**GET /api/orders/{id}/:** Получить информацию о конкретном заказе.<br>
**PUT/PATCH /api/orders/{id}/:** Обновить информацию о заказе.<br>
**DELETE /api/orders/{id}/:** Удалить заказ.<br>
