from django.urls import path
from apps.vendor.views import * 
from apps.accounts import views as AccountViews

urlpatterns = [
    path('',AccountViews.vendorDashboard),
    path('profile/',vprofile,name='vprofile'),
]
