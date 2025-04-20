from django.db import models
from apps.accounts.models import User
from apps.menu.models import FoodItem 
from apps.vendor.models import Vendor
# Create your models here.

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('CREDIT_CARD', 'Credit Card'),
        ('PAYPAL', 'PayPal'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transection_id = models.CharField(max_length=255, unique=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS) 
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transection_id

class Order(models.Model):
    STATUS = (
        ('NEW', 'New'),
        ('ACCEPTED', '  Accepted'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True,blank=True)
    vendor = models.ManyToManyField(Vendor,blank=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15,blank=True)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=15,blank=True)
    city = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=10)
    total = models.FloatField(max_length=10)
    tax_data = models.JSONField(blank=True, help_text = "Data format: {'tax_type':{'tax_percentage':'tax_amount'}}", null=True)
    total_data = models.JSONField(blank=True,null=True) 
    total_tax = models.FloatField()
    payment_method = models.CharField(max_length=25)
    status = models.CharField(max_length=15, choices=STATUS, default='NEW')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Contenate first name and last name
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.order_number 
    
class OrderdFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.fooditem.food_title 
    