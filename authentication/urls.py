from django.urls import path,include
from .views import *

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('signin/',signin,name='signin'),
    path('signout/',signout,name='signout'),
    path('activate/<uidb64>/<token>',activate,name="activate"),
    path('changepassword/',changepassword,name='changepassword'),
    path('forgotpassword/',Forgotpassword,name='forgotpassword'),
    path('otp/',otp,name='otp')
]