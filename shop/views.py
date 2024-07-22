from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def store(request):
    return render(request,"shop/store.html")

def cart(request):
    return render(request,"shop/cart.html")

def checkout(request):
    return render(request,"shop/checkout.html")