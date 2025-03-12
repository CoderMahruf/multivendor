from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.

class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer')
    )
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    username = models.CharField(max_length=50,unique=True)
    email =  models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=15,blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE,default=CUSTOMER)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)
    

class UserProfile(AbstractBaseUser):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(upload_to='user_images/')
    cover_photo = models.ImageField(upload_to='user_images/')
    address = models.CharField(max_length=50,blank=True,null=True)
    zilla = models.CharField(max_length=15,blank=True,null=True)
    latitude = models.CharField(max_length=20,blank=True,null=True)
    longitude = models.CharField(max_length=20,blank=True,null=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return str(self.id)
    