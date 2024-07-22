from django.urls import path,include
from .views import *
from authentication.views import *

urlpatterns = [
    path('',index,name="index"),
    path('brush/',brush,name="brush"),
    path('cart/',cart,name="cart"),]