from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse ,JsonResponse
import simplejson as json 
from apps.marketplace.models import Cart
from apps.marketplace.context_processors import get_cart_amounts
from .forms import OrderForm 
from .models import Order, Payment , OrderdFood
from .utils import generate_order_number,order_total_by_vendor
from apps.accounts.utils import send_notification 
from apps.marketplace.models import Tax
from apps.menu.models import FoodItem
# Create your views here.

@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)
    
    get_tax = Tax.objects.filter(is_active=True)
    subtotal = 0
    total_data = {}
    k = {}
    for i in cart_items:
        fooditem = FoodItem.objects.get(pk=i.fooditem.id,vendor_id__in=vendors_ids)
        v_id = fooditem.vendor.id 
        if v_id in k:
            subtotal = k[v_id]
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal
        else:
            subtotal += (fooditem.price * i.quantity)
            k[v_id] = subtotal

        # calculate the tax_data
        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_parcentage = i.tax_parcentage
            tax_amount = round((tax_parcentage * subtotal)/100,2)
            tax_dict.update({tax_type:{str(tax_parcentage):str(tax_amount)}})
        # Construct total data 
        total_data.update({fooditem.vendor.id:{str(subtotal):str(tax_dict)}})
    
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code'] 
            order.user = request.user
            order.total = grand_total 
            order.tax_data = json.dumps(tax_data) 
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax 
            order.payment_method = request.POST.get('payment_method')
            order.save()  # order id/pk is generated here 
            order.order_number = generate_order_number(order.id)
            order.vendors.add(*vendors_ids)
            order.save()
            context = {
                'order':order,
                'cart_items':cart_items, 
            }
            return render(request, 'orders/place_order.html',context)

        else:
            print(form.errors)
    return render(request, 'orders/place_order.html')

@login_required(login_url='login')
def payments(request):
    # Check if the request AJAX or not 
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # Store the payment details in the payment model 
        order_number = request.POST.get('order_number')
        transaction_id = request.POST.get('transaction_id')
        payment_method = request.POST.get('payment_method')
        status = request.POST.get('status') 
        order = Order.objects.get(user = request.user,order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            payment_method = payment_method,
            amount = order.total,
            status = status 
        )
        payment.save()
        # Update the order model 
        order.payment = payment
        order.is_ordered = True
        order.save()
        # Move the cart itmes to orderd food model 
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            ordered_food = OrderdFood()
            ordered_food.order = order 
            ordered_food.payment = payment
            ordered_food.user = request.user 
            ordered_food.fooditem = item.fooditem 
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price 
            ordered_food.amount = item.fooditem.price * item.quantity # total amount 
            ordered_food.save()

        # Send order confirmation email to the customer 
        mail_subject = 'Thank you for ordering with us.'
        mail_template = 'orders/order_confirmation_email.html'
        ordered_food = OrderdFood.objects.filter(order=order)
        customer_subtotal = 0
        for item in ordered_food:
            customer_subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'user':request.user,
            'order':order,
            'to_email':order.email,
            'ordered_food':ordered_food,
            'domain':get_current_site(request),
            'customer_subtotal':customer_subtotal,
            'tax_data':tax_data
        }
        send_notification(mail_subject,mail_template,context)

        # Send order Received email to the vendor 
        mail_subject = 'You have received a new order'
        mail_template = 'orders/new_order_received.html'
        to_emails  = []
        for i in cart_items:
            if i.fooditem.vendor.user.email not in to_emails:
                to_emails.append(i.fooditem.vendor.user.email)
                ordered_food_to_vendor = OrderdFood.objects.filter(order=order,fooditem__vendor=i.fooditem.vendor)
                print(ordered_food_to_vendor)
                context = {
                    'order':order,
                    'to_email': to_emails,
                    'ordered_food_to_vendor':ordered_food_to_vendor,
                    'vendor_subtotal':order_total_by_vendor(order, i.fooditem.vendor.id)['subtotal'],
                    'tax_data': order_total_by_vendor(order, i.fooditem.vendor.id)['tax_dict'],
                    'vendor_grand_total': order_total_by_vendor(order, i.fooditem.vendor.id)['grand_total']
                }
                send_notification(mail_subject,mail_template,context)

        # Clear the cart if the payment is successful
        # cart_items.delete()

        # Retrurn back to ajax with the status success or failure 
        response = {
            'order_number':order_number,
            'transaction_id':transaction_id,
        }
        return JsonResponse(response)
    return JsonResponse('Payments view') 

def order_complete(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    try:
        order = Order.objects.get(order_number=order_number,payment__transaction_id=transaction_id,is_ordered=True)
        ordered_food = OrderdFood.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        print(tax_data)
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        return render(request,'orders/order_complete.html',context)
    except:
        return redirect('home')