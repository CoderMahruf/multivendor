from  django.urls import path
from .views import * 

urlpatterns = [
    path('place-order/', place_order, name='place_order'),
]