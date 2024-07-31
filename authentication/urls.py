from django.urls import path,include
from .views import *
from django.contrib.auth import views 

urlpatterns = [
    path('signup/',signup,name='signup'),
    path('signin/',signin,name='signin'),
    path('signout/',signout,name='signout'),
    path('activate/<uidb64>/<token>',activate,name="activate"),
    path('changepassword/',changepassword,name='changepassword'),
    path('myprofile/',myprofile,name='myprofile'),
    path('edit/',myprofile_edit,name='edit'),
    #path('forgotpassword/',Forgotpassword,name='forgotpassword'),
    #path('otp/',otp,name='otp')
    path('password_reset/',views.PasswordResetView.as_view(template_name='authentication/forgotpassword.html'),name='password_reset'),
    path('password_reset_done/',views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_done.html"),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>',views.PasswordResetConfirmView.as_view(template_name='authentication/password_reset_confirm.html'),name='password_reset_confirm'), 
    path('password_reset_complete/',views.PasswordResetCompleteView.as_view(template_name='authentication/forgotpassword_reset_complete.html'),name='password_reset_complete'),
]