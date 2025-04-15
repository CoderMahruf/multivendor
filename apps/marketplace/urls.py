from django.urls import path 
from .views import * 
urlpatterns = [
    path('',marketplace,name='marketplace'),
    path('<slug:vendor_slug>/',vendor_detail,name='vendor_detail'),

    # Add to Cart
    path('add_to_cart/<int:food_id>/',add_to_cart,name='add_to_cart'),
    # DECREASE CART
    path('decrease_cart/<int:food_id>/',decrease_cart,name='decrease_cart'),
    # DELETE CART ITEM
    path('delete_cart/<int:cart_id>/',delete_cart,name='delete_cart'),
]
