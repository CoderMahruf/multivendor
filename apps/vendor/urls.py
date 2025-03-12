from django.urls import path
from .views import *
urlpatterns = [
    path('register-restaurent',RgisterRestaurent.as_view(),name='register-restaurent'),
    path('restaurent',Restaurent.as_view(),name='restaurent')
]
