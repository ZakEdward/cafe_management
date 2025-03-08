from .models import Order

class RevenueService:
    @staticmethod
    def calculate_revenue():
        paid_orders = Order.objects.filter(status='paid')
        total_revenue = sum(order.total_price for order in paid_orders)
        return total_revenue