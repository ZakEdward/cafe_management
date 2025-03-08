from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest
from django.http import Http404
from .models import Order
from .forms import OrderForm
from .services import RevenueService

def order_list(request):
    """
    Отображает список всех заказов с возможностью фильтрации и поиска.
    """
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '').strip()

    # Начинаем с полного списка заказов
    orders = Order.objects.all()

    # Применяем фильтр по статусу
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Применяем поиск
    if query:
        # Словарь для перевода русских статусов в значения базы данных
        status_translation = {
            'в ожидании': 'pending',
            'готово': 'ready',
            'оплачено': 'paid',
        }

        # Проверяем, является ли запрос статусом на русском
        translated_status = status_translation.get(query.lower())

        if translated_status:
            # Если запрос соответствует статусу, фильтруем по нему
            orders = orders.filter(status=translated_status)
        else:
            # Иначе ищем по номеру стола
            orders = orders.filter(table_number__icontains=query)

    context = {'orders': orders}
    return render(request, 'orders/order_list.html', context)
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Проверяем, что список блюд не пуст
            items = form.cleaned_data.get('items')
            if not items:
                form.add_error('items', 'Добавьте хотя бы одно блюдо.')
                return render(request, 'orders/add_order.html', {'form': form})
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/add_order.html', {'form': form})

def update_order(request, order_id):
    """
    Редактирование заказа (обновление статуса и списка блюд).
    """
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        # Проверяем, изменился ли список блюд для оплаченного заказа
        submitted_items = request.POST.get('items')
        if order.status == 'paid' and submitted_items != order.items:
            return HttpResponseBadRequest("Нельзя изменять список блюд для оплаченного заказа.")

        # Обрабатываем форму
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)

    return render(request, 'orders/edit_order.html', {'order': order, 'form': form})

def revenue_report(request):
    total_revenue = RevenueService.calculate_revenue()
    return render(request, 'orders/revenue.html', {'total_revenue': total_revenue})

def delete_order(request, order_id):
    """Удаление заказа."""
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        raise Http404("Заказ не найден.")
    order.delete()
    return redirect('order_list')