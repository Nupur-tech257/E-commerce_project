from django import forms 

class SignupForm(forms.Form):
    first_name=forms.CharField(label="First Name",max_length=50,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter name"})
    last_name=forms.CharField(label="Last Name",max_length=50,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter name"})
    email=forms.EmailField(label="Eamil Address",error_messages={"required":"This can't be empty!"})
    password=forms.CharField(label="Password",widget=forms.PasswordInput,max_length=15,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter Password"},help_text="maximum length of password is 15.Please do not exceed this limit")
    confirm_password=forms.CharField(label="Confirm Password",widget=forms.PasswordInput,error_messages={"required":"This can't be empty!"})

class SigninForm(forms.Form):
    username=forms.CharField(label="Username")
    password=forms.CharField(label="Password",widget=forms.PasswordInput)

class ChangePassword(forms.Form):
    password=forms.CharField(label="Password",widget=forms.PasswordInput,max_length=15,
                               error_messages={"required":"This can't be empty!",
                                               "max_length":"Enter a shorter Password"},help_text="maximum length of password is 15.Please do not exceed this limit")
    confirm_password=forms.CharField(label="Confirm Password",widget=forms.PasswordInput,error_messages={"required":"This can't be empty!"})

class OTP(forms.Form):
    otp=forms.IntegerField(label="OTP",max_value=4)