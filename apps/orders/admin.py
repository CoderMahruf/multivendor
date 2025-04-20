from django.contrib import admin
from .models import Order, OrderdFood, Payment
# Register your models here.

# class OrderFoodInline(admin.TabularInline):
    # model = OrderdFood
    # readonly_fields = ('order', 'payment','user', 'fooditem', 'quantity', 'price', 'amount')
    # extra = 0

# class OrderAdmin(admin.ModelAdmin):
    # list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status','order_placed_to','is_ordered']
    # inlines = [OrderFoodInline]

admin.site.register(Order)
admin.site.register(OrderdFood)
admin.site.register(Payment)