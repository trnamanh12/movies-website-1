from .views import add_to_cart, remove_from_cart, checkout, view_cart, update_cart_item_quantity
from django.urls import path

urlpatterns = [
    path('add-to-cart/<int:ticket_id>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('update-cart-item-quantity/<int:item_id>/', update_cart_item_quantity, name='update_cart_item_quantity'),
]