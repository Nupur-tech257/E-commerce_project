from django.urls import path,include
from .views import *
from authentication.views import *
from authentication.urls import *

urlpatterns = [
    path('',main,name="main"),
    path('store/',store,name="store"),
    path('cart/',cart,name="cart"),
    path('checkout/',checkout,name="checkout"),
    path('update/',updateitem,name="update"),
    path('process_order/',processOrder,name='process_order')]