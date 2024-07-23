from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def main(request):
    return render(request,"shop/main.html")

def store(request):
    fname=request.user.first_name
    product=Product.objects.all()
    context={"product":product,"fname":fname}
    return render(request,"shop/store.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
    context={'items':items}
    print(context)
    return render(request,"shop/cart.html",context)

def checkout(request):
    return render(request,"shop/checkout.html")