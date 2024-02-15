from django.contrib import admin
from .models import Pet, Order, OrderItem, Customer, ShippingAddress


class PetAdmin(admin.ModelAdmin):
    list_display = ("gender", "image", "name", "breed", "description",)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "date_ordered", "complete", "transaction_id")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("product", "order", "quantity", "date_added")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ("customer", "order", "street", "city", "state", "zipcode", "date_added")


admin.site.register(Pet, PetAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(ShippingAddress,ShippingAddressAdmin)
