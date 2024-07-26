from .models import *
import json

def cookiecart(request):
    try:
        cart=json.loads(request.COOKIES["cart"])
    except: 
        cart={}
    print(cart)
    items=[]
    order_items=0
    order_total=0
    for i in cart:
        try:
            order_items+=cart[i]['quantity']
            product=Product.objects.get(id=i)
            total=product.price*cart[i]['quantity']
            order_total+=total

            item={'product':{'id':product.id,
                             'name':product.name,
                             'imageURL':product.imageURL,
                             'price':product.price,},
                  'quantity':cart[i]['quantity'],
                  'get_total':total,}
            items.append(item)
        except:
            pass
    return items,order_items,order_total

def data(request):
    if request.user.is_authenticated:
        customer=request.user
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
        order_items=order.get_cart_item
        order_total=order.get_cart_total
        fname=request.user.first_name
    else:
        items,order_items,order_total= cookiecart(request)
        fname=""
    return items,order_items,order_total,fname