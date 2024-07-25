from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import json
import datetime

# Create your views here.
def main(request):
    return render(request,"shop/main.html")

def store(request):
    product=Product.objects.all()
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        print('s')
        items=order.orderitem_set.all()
        order_items=order.get_cart_item
        fname=request.user.first_name
        context={"product":product,"fname":fname,"order_items":order_items}
        return render(request,"shop/store.html",context)
    else:
        items=[]
        order_items=0
        context={"product":product,"order_items":order_items}
        return render(request,"shop/store.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        order_items=order.get_cart_item
        order_total=order.get_cart_total
    else:
        items=[]
        order_items=0
        order_total=0

    context={'items':items,"order_items":order_items,"order_total":order_total}
    print(context)
    return render(request,"shop/cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        order_items=order.get_cart_item
        order_total=order.get_cart_total
    else:
        items=[]
        order_items=0
        order_total=0

    context={'items':items,"order_items":order_items,"order_total":order_total}
    return render(request,"shop/checkout.html",context)

def updateitem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']

    customer=request.user
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created=OrderItem.objects.get_or_create(order=order,product=product)
    if action=='add':
        orderitem.quantity=(orderitem.quantity+1)
    elif action=='remove':
        orderitem.quantity=(orderitem.quantity-1)
    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()
    print(orderitem.quantity)
    return JsonResponse('item',safe=False)

def processOrder(request):
    data=json.loads(request.body)
    transaction_id=datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        order_total=order.get_cart_total
        print(order_total)
        order.transaction_id=transaction_id
        order.complete=True
        print(order_total)
        print(order.transaction_id)
        order.save()
        ShippingAddresss.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            #date_added=datetime.datetime.now()
            )
        print(order_total)
    else:
        print("user is not logged in")

    return JsonResponse('Payment complete',safe=False)