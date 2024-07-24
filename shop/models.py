from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.FloatField(default=0)
    image=models.ImageField(null=True,blank=True)

    def __str__(self):
        return f'{self.name}'
    
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=" "
        return url

class Order(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
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
        return total


    def __str__(self) -> str:
        return f'{self.id}.{self.customer}'
    
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total

    def __str__(self) -> str:
        return f'{self.id}.{self.order}'

class ShippingAddresss(models.Model):
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.address)
    
