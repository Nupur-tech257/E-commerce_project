from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
import authentication
from myshop import settings
from .forms import *

# Create your views here.
def home(request):
    return HttpResponse("hello")

def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            fname=form.cleaned_data['first_name']
            lname=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            password1=form.cleaned_data['password'] 
            password2=form.cleaned_data['confirm_password']
            full_name = "%s %s" % (fname, lname)
            username=full_name.strip()


            if User.objects.filter(email=email):
                msg="Email already registered!"
                return render(request,'authentication/signup.html',{"msg":msg,"form":form})
        
            if password1!=password2:
                msg="passwords didn't match"
                return render(request,'authentication/signup.html',{"msg":msg,"form":form})

            myuser=User.objects.create_user(username,email,password1)
            myuser.first_name=fname
            myuser.last_name=lname
            myuser.save()

        #Welcome Email 
            subject="Welcome!"
            message="Hello"+myuser.first_name+"!"+"\n"+"Welcome to our site \n Thank you for registering"
            from_email=settings.EMAIL_HOST_USER
            to_list=[myuser.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)
            return redirect('signin')
    else:
        form=SignupForm()

        
    return render(request,'authentication/signup.html',{"form":form})

def signin(request):
    if request.method=='POST':
        form=SigninForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            print(username,password)
            user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            fname=user.first_name
            print(fname)
            return render(request,"authentication/index.html",context={"fname":fname})
        else:
            message="You've entered wrong username or password"
            return render(request,'authentication/signin.html',{"message":message,"form":form})
    else:
        form=SigninForm()
    return render(request,'authentication/signin.html',{"form":form})

def signout(request):
    logout(request)
    message="you've logged out successfully!"
    return render(request,'authentication/signout.html',{"message":message})