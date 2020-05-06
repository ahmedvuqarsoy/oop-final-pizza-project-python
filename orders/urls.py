from django.urls import include, path
from django.conf.urls import url
from .views import OrderCreateView
from . import views

urlpatterns = [
    path('', views.home, name='orders-home'),
    path('orders/create/', OrderCreateView.as_view(), name='orders-create'),
    path('orders/history/', views.order_history, name='orders-history'),
    path('ajax/load-meal_type/', views.load_meal_type, name='ajax_load_meal_type'),
    path('ajax/load-size/', views.load_size, name='ajax_load_size'),
    path('ajax/load-meal_addition/', views.load_meal_addition, name='ajax_load_meal_addition'),
    path('ajax/load-price/', views.load_price, name='ajax_load_price')
]
