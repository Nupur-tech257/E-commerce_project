from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth import authenticate,login,logout
from myshop import settings
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .tokens import *
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import random,time
import http.client
from myshop.settings import AUTH_KEY
from shop.models import *

# Create your views here.

def signup(request):
    '''this function is for users to signup on our website.
    user details is stored in inbuilt User model'''
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            fname=form.cleaned_data['first_name']
            lname=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phonenumber=form.cleaned_data['phonenumber']
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
            profile=Profile(user=myuser,phonenumber=phonenumber)
            profile.save()

        #Welcome Email 
            '''subject="Welcome!"
            message="Hello"+myuser.first_name+"!"+"\n"+"Welcome to our site \n Thank you for registering"
            from_email=settings.EMAIL_HOST_USER
            to_list=[myuser.email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)'''

        # Confirmation mail
            '''this sends a confirmation mail to user on their registered email and activate the user '''
            current_site=get_current_site(request)
            email_subject="Email Confirmation"
            message2=render_to_string("email_confirmation.html",{
                "name":myuser.first_name,
                "domain":current_site.domain,
                "uid":urlsafe_base64_encode(force_bytes(myuser.pk)),
                "token":generate_token.make_token(myuser)
            })
            email=EmailMessage(
                email_subject,message2,settings.EMAIL_HOST_USER,[myuser.email],)
            email.fail_silently=True
            email.send()


            return redirect('signin')
    else:
        form=SignupForm()

        
    return render(request,'authentication/signup.html',{"form":form})

def signin(request):
    '''this function is for user to signin'''
    if request.method=='POST':
        form=SigninForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            fname=user.first_name
            return redirect("store")
        else:
            message="You've entered wrong username or password"
            return render(request,'authentication/signin.html',{"message":message,"form":form})
    else:
        form=SigninForm()
    return render(request,'authentication/signin.html',{"form":form})

def signout(request):
    '''this function is for user to signout'''
    logout(request)
    return redirect('signin')
   

def activate(request,uidb64,token):
    '''after a confirmation link is sent to user this functions activates his account'''
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect("home")
    else:
        return render(request,"activation_failed.html")
    
def changepassword(request):
    user=request.user
    if request.method=='POST':
        form=ChangePassword(request.POST)
        if form.is_valid():
            old_password=form.cleaned_data['old_password']
            new_password=form.cleaned_data['new_password']
            confirm_password=form.cleaned_data['confirm_password']

        if new_password!=confirm_password:
            message="passwords don't match"
            return render(request,'authentication/changepassword.html',{"message":message,"form":form})
        
        if check_password(old_password,user.password):
            user.set_password(new_password)
            user.save()
            message='Password changed'
            form=SigninForm()
            return render(request,'authentication/signin.html',{'form':form,'message':message})
        else:
            message="Old password is Incorrect"
            return render(request,'authentication/changepassword.html',{"message":message,"form":form})
    else:
        form=ChangePassword()
    return render(request,'authentication/changepassword.html',{"form":form})

def myprofile_edit(request):
    user=request.user
    profile=Profile.objects.get(user=user)
def send_otp(mobile,otp):
    conn = http.client.HTTPSConnection("control.msg91.com")
    headers = { 'Content-Type': "application/JSON" }
    conn.request("POST", f"/api/v5/otp?otp="+otp+"&otp_length=4&otp_expiry=1&template_id=ABC&mobile="+mobile+"&authkey=427321AdlqGzr3GHp66a8c69fP1", headers)
    res = conn.getresponse()
    data = res.read()
    return None

'''def Forgotpassword(request):
    if request.method=='POST':
        form=Myprofile(request.POST)
        if form.is_valid():
            f_name=form.cleaned_data['first_name']
            l_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            phn=form.cleaned_data['phonenumber']
        if f_name=="":
            f_name=user.first_name
        if l_name=="":
            l_name=user.last_name
        if username=="":
            username=user.username
        if email=="":
            email=user.email
        if phn=="":
            phn=profile.phonenumber
           
        User.objects.filter(id=user.id).update(first_name=f_name,last_name=l_name,username=username,email=email)
        Profile.objects.filter(user=user).update(phonenumber=phn)
        return redirect('myprofile')
    else:
        form=Myprofile()

    context={'form': form}
    return render(request,'authentication/myprofile_edit.html',context)'''

def myprofile(request):
    user=request.user
    profile=Profile.objects.get(user=user)
    if request.method=='GET':
        f_name=user.first_name
        l_name=user.last_name
        username=user.username
        email=user.email
        phonenumber=profile.phonenumber
        print(phonenumber)
        context={'f_name':f_name,'l_name':l_name,'username':username,'email':email,'phn':phonenumber}
    return render(request,'authentication/myprofile.html',context)
