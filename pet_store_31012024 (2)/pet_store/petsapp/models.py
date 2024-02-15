from django.db import models
from django.contrib.auth.models import User

gender = (('Male', 'Male'), ('Female', 'Female'))


class Pet(models.Model):
    name = models.CharField(max_length=10)
    price = models.IntegerField(default=0)
    breed = models.CharField(max_length=10)
    gender = models.CharField(max_length=6, choices=gender)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media')

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=10, default="NA")

    def __str__(self):
        return self.user.username


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    building_name = models.CharField(max_length=200, null=False)
    street = models.CharField(max_length=200, null=False)
    landmark = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    zipcode = models.CharField(max_length=6, null=False)
    date_added = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    product = models.ForeignKey(Pet, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_cost(self):
        return self.price * self.quantity


class CartItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='pets')
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = "cart_items"
        ordering = ('pet',)

    def __str__(self):
        return self.pet.name
