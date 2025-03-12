from django.urls import path
from .views import *
urlpatterns = [
    path('user-registration',UserRegistration.as_view(),name='user-registration')
]
