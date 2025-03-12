from django.shortcuts import render
from django.views import View

# Create your views here.
class UserRegistration(View):
    def get(self,request):
        return render (request, 'users/registration.html')