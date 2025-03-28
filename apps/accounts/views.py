from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserForm 
from .models import User
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,'Your account has been registered successfully !')
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request,'accounts/registerUser.html',{'form':form})