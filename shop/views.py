from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def brush(request):
    return render(request,"shop/brush.html")

def cart(request):
    return render(request,"shop/cart.html")
