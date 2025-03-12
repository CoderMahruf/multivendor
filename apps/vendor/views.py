from django.shortcuts import render
from django.views import View
# Create your views here.

class RgisterRestaurent(View):
    def get(self,request):
        return render(request,'vendor/register-restaurant.html')
    
class Restaurent(View):
    def get(self,request):
        return render(request, 'vendor/listing-detail.html')