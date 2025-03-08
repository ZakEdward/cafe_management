from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'items', 'status']

    def clean_items(self):
        """
        Валидация данных из скрытого поля items_json.
        """
        items = self.cleaned_data.get('items')
        if not isinstance(items, list):
            raise forms.ValidationError("Список блюд должен быть в формате JSON.")
        for item in items:
            if not isinstance(item, dict) or 'name' not in item or 'price' not in item:
                raise forms.ValidationError("Каждое блюдо должно содержать поля 'name' и 'price'.")
        return items