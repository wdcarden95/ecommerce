// Set variable updateBtns to query set of our buttons
var updateBtns = document.getElementsByClassName('update-cart')

// For loop listens for button clicks from store.html to add items to cart
for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    // log to the console which items are being added, like "productId: 1 action add"
    console.log('productId:', productId, 'action:', action)

    // log to the console if the user adding items to cart is authenticated or not based on main.html
    console.log('USER:', user)
    if (user == 'AnonymousUser'){
      console.log('User is not authenticated')
    }else{
      // call updateUserOrder if authenticated user adds items to cart
      updateUserOrder(productId, action)
    }
  })
}

// Send data for updating the order to the view in views.py
function updateUserOrder(productId, action){
  console.log('User is authenticated, sending data...')

  // Goes to path created in urls.py
  var url = '/update_item/'

  // pass in url to send data to, then define what type of data to send
  fetch(url, {
    // POST data is the type
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      // pass csrf token into fetch() call
      'X-CSRFToken':csrftoken,
    },
    // body is the data sent to the back end; we prepare the data as an object
    // data must be sent as a string; object output is converted to string with stringify
    body:JSON.stringify({'productId':productId, 'action':action})
  })
  // data is now sent; return a promise response after data is sent to view
  // defined in updateItem in view.py as "return JsonResponse"
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    // reload the page once our call returns as successful to see changes
    console.log('data', data)
    // change in the future to use js so page doesn't have to reload
    location.reload()
  });
}
