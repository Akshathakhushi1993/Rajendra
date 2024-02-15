var updateBtns= document.getElementsByClassName('update-cart')
for(var i=0;i<updateBtns.length;i++){
updateBtns[i].addEventListener('click',function(){
var productId=this.dataset.product
var action=this.dataset.action
console.log('productId:',productId,'action:',action)
//gives the user name
console.log('User:',user)
//check above one and type
//this is going to say where user has been logged in or not from admin
if(user=='AnonymousUser'){
console.log('Not logged in')
}
else
{
//instead od passing the msg here we are going to write the sperate function below
updateUserOrder(productId,action)
}
})
}
function updateUserOrder(productId,action){
console.log('User is authenticated,sending data.....')
//once above code is done we have to fetch the data using post method
var url='/update_item/'

//we are saying that we need to update in urls and views 
//to send our post data we use fetch
fetch(url,{
    method:'POST',
    headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
            },
    body:JSON.stringify({'productId':productId,'action':action})
})
.then((response)=>{
return response.json()
})
.then((data)=>{
    console.log('Data:',data)
});
}


