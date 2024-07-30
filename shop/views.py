from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import *
import json
import datetime
from .utils import *
from authentication.forms import *

# Create your views here.
def main(request):
    category=Category.objects.all()
    print(category)
    return render(request,"shop/main.html",{'category':category})

def store(request):
    category=Category.objects.all()
    product=Product.objects.all()
    _,order_items,_,fname= data(request)
    context={"product":product,"fname":fname,"order_items":order_items,'category':category}
    return render(request,"shop/store.html",context)

def cart(request):
    items,order_items,order_total,_= data(request)
    category=Category.objects.all()
    context={'items':items,"order_items":order_items,"order_total":order_total,'category':category}
    return render(request,"shop/cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        order_items=order.get_cart_item
        order_total=order.get_cart_total
        category=Category.objects.all()
        context={'items':items,"order_items":order_items,"order_total":order_total,'category':category}
        return render(request,"shop/checkout.html",context)
    else:
        form=SignupForm()
        return render(request,"authentication/signup.html",{"form":form})

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
    elif action=='delete':
        orderitem.quantity=0
    orderitem.save()
    if orderitem.quantity<=0:
        orderitem.delete()
    return JsonResponse('item',safe=False)

def processOrder(request):
    data=json.loads(request.body)
    transaction_id=datetime.datetime.now().timestamp()
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        order_total=order.get_cart_total
        order.transaction_id=transaction_id
        order.complete=True
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
    else:
        print("user is not logged in")

    return JsonResponse('Payment complete',safe=False)

def search(request):
    if request.method=='POST':
        query=request.POST.get('search')
        print(query)
        product=Product.objects.filter(product_details__icontains=query)
        _,order_items,_,fname= data(request)
    context={"product":product,"fname":fname,"order_items":order_items}
    return render(request,"shop/store.html",context)

def category(request,name):
    if request.method=='GET':
        category=Category.objects.filter(name=name)
        print(category)
        product=Product.objects.filter(category__in=category)
        _,order_items,_,fname= data(request)
        category=Category.objects.all()
    context={"product":product,"fname":fname,"order_items":order_items,'category':category}
    return render(request,"shop/store.html",context)

def views(request,id):
    if request.method=='GET':
        product=Product.objects.filter(id=id)
        _,order_items,_,fname= data(request)
        category=Category.objects.all()
    context={"product":product,"fname":fname,"order_items":order_items,'category':category}
    return render(request,"shop/view.html",context)



