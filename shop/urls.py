from django.urls import path,include
from .views import *
from authentication.views import *

urlpatterns = [
    path('',index,name="index"),
    path('store/',store,name="store"),
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),]