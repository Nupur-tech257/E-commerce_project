var updatebtns=document.getElementsByClassName('update-cart')

for(i=0;i<updatebtns.length;i++){
updatebtns[i].addEventListener('click',function()
   {
    var productId=this.dataset.product
    var action=this.dataset.action
    console.log('productId:',productId,"Action:",action)
    
    console.log("User:",user)
    if (user==="AnonymousUser")
        {alert("please signup first")}
        //{addcookieItem(productId,action)}
    else
        {updateUserorder(productId,action)}
    })
}

function addcookieItem(productId,action){
    if (action=="add"){
        if(cart[productId]==undefined){
            cart[productId]={'quantity':1}
        }
        else{
            cart[productId]['quantity']+=1
        }
    }
    if(action=="remove"){
        cart[productId]['quantity']-=1
        if(cart[productId]['quantity']<=0){
            delete cart[productId]
            console.log('remove item')
        }
    }
    document.cookie='cart='+JSON.stringify(cart)+ ";domain=;path=/"
    location.reload()
}

function updateUserorder(productId,action){
    console.log("user is authenticated")
    var url='/update/'
    fetch(url,{method:'POST',
               headers:{"Content-Type":"application/json",
                        "X-CSRFToken":csrftoken,
               },
               body:JSON.stringify({"productId":productId,"action":action})
    })
    .then((response)=>{return response.json()})
    .then((data)=>{console.log('Data:',data)
                   location.reload()
    });
}