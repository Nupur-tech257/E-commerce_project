from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.name}'
    
class Vendor(models.Model):
    name=models.CharField(max_length=50)
    phone_number=models.IntegerField(unique=True)
    email=models.EmailField(unique=True)

    def __str__(self):
        return str(self.name)
    
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    phonenumber=PhoneNumberField(blank=True)
    

class Product(models.Model):
    #vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200)
    price=models.FloatField(default=0)
    product_details=models.TextField(blank=True)
    image=models.ImageField(null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    discount=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f'{self.name}'
    
    @property
    def price_after_discount(self):
        if self.discount is not None:
            price1=self.price-(self.price*(self.discount/100))
        return round(price1,2)
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=" "
        return url

class Order(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    date_ordered=models.DateField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=200,null=True)

    @property
    def get_cart_item(self):
        OrderItems=self.orderitem_set.all()
        print(OrderItems)
        total=sum([ i.quantity for i in OrderItems])
        return total
    
    @property
    def get_cart_total(self):
        OrderItems=self.orderitem_set.all()
        print(OrderItems)
        total=sum([ i.get_total for i in OrderItems])
        return round(total,2)


    def __str__(self) -> str:
        return f'{self.id}.{self.customer}'
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product.discount is None:
            total=self.product.price*self.quantity
        else:
            price=self.product.price-(self.product.price*(self.product.discount/100))
            total=price*self.quantity
        return round(total,2)

    def __str__(self) -> str:
        return f'{self.id}.{self.order}'

class ShippingAddresss(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.address)
    
