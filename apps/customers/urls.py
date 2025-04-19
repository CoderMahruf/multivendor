from django.urls import path 
from apps.accounts import views as AccountViews 
from .views import * 
urlpatterns = [
    path('',AccountViews.custDashboard,name='customer'),
    path('profile/',cprofile,name='cprofile'),
]
