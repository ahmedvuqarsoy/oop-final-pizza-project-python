from django.conf.urls import url
from django.urls import path

from .views import (add_to_cart, delete_from_cart, order_details, checkout, success, update_transaction_records)

app_name = 'shopping_cart'

urlpatterns = [
    path('add-to-cart/', add_to_cart, name="add_to_cart"),
    path('order-summary/', order_details, name="order_summary"),
    path('success/', success, name="purchase_success"),
    #url(r'^success/$', success, name='purchase_success'),
    path('item/delete/<int:item_id>/', delete_from_cart, name="delete_item"),
    #url(r'^item/delete/(?P<item_id>[-\w]+)/$', delete_from_cart, name='delete_item'),
    path('checkout/', checkout, name="checkout"),
    path('update-transaction/<str:token>/', update_transaction_records, name='update_records'),
]