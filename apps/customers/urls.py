from django.urls import path 
from apps.accounts import views as AccountViews 
from .views import * 
urlpatterns = [
    path('',AccountViews.custDashboard,name='customer'),
    path('profile/',cprofile,name='cprofile'),
    path('my_orders/',my_orders,name='customer_my_orders'), 
    path('order_detail/<int:order_number>/',order_detail,name='order_detail'),
]
