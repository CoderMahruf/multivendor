from django.urls import path
from apps.vendor.views import * 
from apps.accounts import views as AccountViews

urlpatterns = [
    path('',AccountViews.vendorDashboard),
    path('profile/',vprofile,name='vprofile'),
    path('menu-builder',menu_builder,name='menu_builder'),
    path('menu-builder/category/<int:pk>/',fooditems_by_category,name='fooditems_by_category'),


    # Category CRUD
    path('menu-builder/category/add',add_category,name='add_category'),
    path('menu-builder/category/edit/<int:pk>/',edit_category,name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/',delete_category,name='delete_category'),

    # FoodItem CRUD
    path('menu-builder/food/add/',add_food,name='add_food'),
    path('menu-builder/food/edit/<int:pk>/',edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/',delete_food, name='delete_food'),

    # Opening Hour CRUD
    path('opening-hours/',opening_hours,name='opening_hours'),
    path('opening-hours/add/',add_opening_hours,name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/',remove_opening_hours,name='remove_opening_hours'),

    path('order_detail/<int:order_number>/',order_detail,name='vendor_order_detail'),
    path('my_orders/',my_orders,name='vendor_my_orders'),
]
