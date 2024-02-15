from django.urls import path

from . import views


urlpatterns = [
    path('list_pets', views.list_pets, name='list_pets'),
    path('pet-detail/<int:id>', views.pet_detail, name='pet_detail'),
    path('', views.user_login),
    path('signup', views.register, name='register'),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('search-pets', views.search_pets, name='search_pets'),
    path('response/<int:order_id>/<int:amount>', views.payment_process, name="response"),

    path('add-to-cart/<int:pet_id>', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pet_id>', views.remove_from_cart, name='remove_from_cart'),
    path('payment-order/', views.payment_order, name="payment_order"),
    path('payment-process/<int:order_id>/<int:amount>', views.payment_process, name="payment_process"),
    path('cart-items', views.cart_items, name='cart_items'),

    # Shipping address URLs
    path('add-address', views.add_address, name='add_address'),
    path('list-addresses', views.list_addresses, name='list_addresses'),
    path('set-delivery-address', views.set_delivery_address, name='set_delivery_address'),
    path('order-review/<int:sa_id>', views.order_review, name='order_review'),
    path('checkout-order/<int:sa_id>', views.checkout_order, name='checkout_order'),
]
