import razorpay
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.contrib import messages

from .forms import UserCustomRegisterForm, CartAddProductForm
from .forms import ShippingAddressForm, UserCustomRegisterForm2
from .forms import SetDeliveryAddressForm
from .models import CartItem
from .cart import Cart
from .models import Pet, Order, OrderItem, Customer, ShippingAddress


def register(request):
    if request.method == 'POST':
        form1 = UserCustomRegisterForm(request.POST)
        form2 = UserCustomRegisterForm2(request.POST)
        print(request.POST)
        print(form1.errors)
        print(form2.errors)
        if form1.is_valid() and form2.is_valid():
            u = form1.save()
            f2 = form2.save(commit=False)
            f2.user = u
            f2.save()
            return redirect('login')
    else:
        form1 = UserCustomRegisterForm()
        form2 = UserCustomRegisterForm2()
    return render(request, 'register.html', {'form1': form1, 'form2': form2})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fn = AuthenticationForm(request=request, data=request.POST)
            if fn.is_valid():
                uname = fn.cleaned_data['username']
                upass = fn.cleaned_data['password']
                u = authenticate(username=uname, password=upass)
                if u is not None:
                    login(request, u)
                return redirect('list_pets')
        else:
            fn = AuthenticationForm()
        return render(request, 'login.html', {'form': fn})
    else:
        return redirect('list_pets')


def list_pets(request):
    template_name = 'list.html'
    pets = Pet.objects.all()
    context = collect_cart_details(request)
    context['pets'] = pets
    return render(request, template_name, context=context)


def pet_detail(request, id):
    template_name = "details.html"
    pet = Pet.objects.get(id=id)
    context = collect_cart_details(request)
    context['pet'] = pet
    return render(request, template_name, context=context)


def add_to_cart(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    customer = Customer.objects.get(user=request.user)
    # Get the cart items for given customer and pet
    existing_cart_items = CartItem.objects.filter(customer__user=request.user, pet=pet)
    if len(existing_cart_items) == 0:
        cart_item = CartItem.objects.create(customer=customer, pet=pet)
    else:
        cart_item = existing_cart_items[0]

    cart_item.quantity = request.POST['quantity']
    cart_item.save()

    return redirect('cart_items')


def collect_cart_details(request):
    cart_items_list = CartItem.objects.filter(customer__user=request.user)
    qty_list = [n for n in range(1, 6)]
    all_items_price = 0
    for item in cart_items_list:
        item.item_price = item.quantity * item.pet.price
        all_items_price = all_items_price + item.item_price

    context = {
        'cart': cart_items_list,
        'total_price': all_items_price,
        'qty_list': qty_list
    }
    return context


def cart_items(request):
    template_name = 'cart_items.html'
    # Collect the cart details
    context = collect_cart_details(request)
    return render(request, template_name, context=context)


def remove_from_cart(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    cart_item = CartItem.objects.get(customer__user=request.user.id, pet=pet)
    cart_item.delete()
    return redirect('cart_items')


# def profile(request):
#     return render(request, 'petsapp/profile.html')


def set_delivery_address(request):
    template_name = "delivery_address.html"
    addr_list = ShippingAddress.objects.filter(customer__user__id=request.user.id)
    if request.method == "POST":
        form = SetDeliveryAddressForm(request.POST)
        if form.is_valid():
            return redirect('order_review', sa_id=form.cleaned_data['delivery_address'])
    else:
        form = SetDeliveryAddressForm()
    context = {
        'address_list': addr_list,
        'form': form
    }
    return render(request, template_name, context=context)


def order_review(request, sa_id):
    template_name = 'order_review.html'
    context = collect_cart_details(request)
    context['sa_id'] = ShippingAddress.objects.get(id=sa_id)
    return render(request, template_name, context=context)


def clear_cart_details(request):
    cart_items_list = CartItem.objects.filter(customer__user=request.user)
    for item in cart_items_list:
        item.delete()


def checkout_order(request, sa_id):
    cart_items_list = collect_cart_details(request)['cart']
    customer = Customer.objects.filter(user=request.user)
    delivery_addr = ShippingAddress.objects.filter(id=sa_id)
    if customer:
        order = Order(customer=customer[0], shipping_address=delivery_addr[0])
        order.save()
        for item in cart_items_list:
            OrderItem.objects.create(
                order=order,
                product=item.pet,
                price=item.pet.price,
                quantity=item.quantity
            )
        # Empty the cart
        clear_cart_details(request)
        # Save order_id for future use in payment order page
        request.session['order_id'] = order.id
        # redirect for payment
        return redirect(reverse('payment_order'))
    else:
        return redirect(reverse('list_pets'))


# Initialize the razorpay client to capture the payment details
client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment_order(request):
    order_id = request.session.get('order_id')
    print("process_order Order is -> ", order_id)
    order = get_object_or_404(Order, id=order_id)
    amount = int(order.get_total_cost()*100)
    amount_inr = amount

    context = {
        'order_id': order_id,
        'public_key': settings.RAZOR_KEY_ID,
        'amount': amount_inr,
        'amountorig': amount
    }
    return render(
        request,
        'created.html',
        context=context
    )


def payment_process(request, order_id, amount):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        order.complete = True
        order.save()
        print("Amount ", amount)
        print("Type amount str to int ", amount)
        payment_id = request.POST['razorpay_payment_id']
        print("Payment Id", payment_id)
        order.transaction_id = payment_id
        order.save()
        payment_client_capture = (client.payment.capture(payment_id, amount))
        print("Payment Client capture", payment_client_capture)
        payment_fetch = client.payment.fetch(payment_id)
        status = payment_fetch['status']
        amount_fetch = payment_fetch['amount']
        amount_fetch_inr = amount_fetch
        print("Payment Fetch", payment_fetch['status'])
        context = {
            'amount': amount_fetch_inr,
            'status': status,
            'transaction_id': payment_id
        }
        return render(request, 'done.html', context=context)


def user_logout(request):
    logout(request)
    return redirect('login')


def add_address(request):
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            sd = form.save(commit=False)
            sd.customer = Customer.objects.get(id=request.POST['customer'])
            sd.save()
            return redirect('list_addresses')
    else:
        form = ShippingAddressForm()
    return render(request, 'add_address.html', {'form': form})


def list_addresses(request):
    template_name = "address.html"
    addr_list = ShippingAddress.objects.filter(customer__user__id=request.user.id)
    context = {
        'addr_list': addr_list
    }
    return render(request, template_name, context=context)


def search_pets(request):
    template_name = "list.html"
    query = request.GET.get('q')
    search_query = Q(name__icontains=query) | Q(breed__icontains=query) | Q(gender__icontains=query)
    pets = Pet.objects.filter(search_query)
    context = collect_cart_details(request)
    context['pets'] = pets
    return render(request, template_name, context=context)
