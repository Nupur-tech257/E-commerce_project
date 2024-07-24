from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from .models import *
import json

# Create your views here.
def main(request):
    return render(request,"shop/main.html")

def store(request):
    product=Product.objects.all()
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
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
    return JsonResponse('item',safe=False)