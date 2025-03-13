from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,  email, password,**extra_fields):

        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password,**extra_fields):
        user = self.create_user(email=email, password=password,**extra_fields)
      
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    SUPERUSER = 3
    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
        (SUPERUSER, 'Superuser'),
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    
    def __str__(self):
        return str(self.id)
    
    USERNAME_FIELD = "email"
    
    class Meta:
        ordering = ['-date_joined']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 3
        super().save(*args, **kwargs)

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
    
    