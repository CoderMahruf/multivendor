from django.urls import path,include
from .views import *

urlpatterns = [
    path('',myAccount),
    path('registerUser/',registerUser,name='registerUser'),
    path('registerVendor/',registerVendor,name='registerVendor'),

    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('myAccount/',myAccount,name='myAccount'),
    path('custDashboard/',custDashboard,name='custDashboard'),
    path('vendorDashboard/',vendorDashboard,name='vendorDashboard'),

    path('activate/<uidb64>/<token>/',activate,name='activate'),

    path('forgot_password/',forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',reset_password_validate,name='reset_password_validate'),
    path('reset_password/',reset_password,name='reset_password'),

    path('vendor/',include('apps.vendor.urls')),
    path('customer/',include('apps.customers.urls')),
]
