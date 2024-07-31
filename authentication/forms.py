from django import forms 
from phonenumber_field.formfields import PhoneNumberField

class SignupForm(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=50,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter name"})
    last_name=forms.CharField(label="Last Name",max_length=50,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter name"})
    email=forms.EmailField(label="Email Address",error_messages={"required":"This can't be empty!"})
    phonenumber = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':('Phone')}),label="Phone number", required=False)
    password=forms.CharField(label="Password",widget=forms.PasswordInput,max_length=15,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter Password"},help_text="maximum length of password is 15.Please do not exceed this limit")
    confirm_password=forms.CharField(label="Confirm Password",widget=forms.PasswordInput,error_messages={"required":"This can't be empty!"})

class SigninForm(forms.Form):
    username=forms.CharField(label="Username")
    password=forms.CharField(label="Password",widget=forms.PasswordInput)

class ChangePassword(forms.Form):
    old_password=forms.CharField(label="Old Password",widget=forms.PasswordInput,max_length=15,
                               error_messages={"required":"This can't be empty!"})
    new_password=forms.CharField(label="New Password",widget=forms.PasswordInput,max_length=15,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter Password"},help_text="maximum length of password is 15.Please do not exceed this limit")
    confirm_password=forms.CharField(label="Confirm Password",widget=forms.PasswordInput,error_messages={"required":"This can't be empty!"})

class OTP(forms.Form):
    otp=forms.IntegerField(label="OTP",max_value=4)

class ForgotPasswordform(forms.Form):
    phonenumber=PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':('Phone')}),label="Phone number", required=False)

class Myprofile(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=50,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter name"},required=False)
    last_name=forms.CharField(label="Last Name",max_length=50,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter name"},required=False)
    email=forms.EmailField(label="Email Address",error_messages={"required":"This can't be empty!"},required=False)
    username=forms.CharField(label="Username",max_length=50,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter name"},required=False)
    phonenumber = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':('Phone')}),label="Phone number", required=False)