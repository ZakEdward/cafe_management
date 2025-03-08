from django.urls import path
from . import views
from .api_views import OrderListCreateView, OrderRetrieveUpdateDestroyView

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('add/', views.add_order, name='add_order'),
    path('delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('update/<int:order_id>/', views.update_order, name='update_order'),
    path('revenue/', views.revenue_report, name='revenue_report'),
    path('api/orders/', OrderListCreateView.as_view(), name='api_order_list'),
    path('api/orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='api_order_detail'),
]