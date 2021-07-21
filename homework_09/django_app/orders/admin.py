from django.contrib import admin
from .models import (
    Buyer,
    Shop,
    PricesType,
    Price,
    Order,
    OrdersProduct,
    Product,
    Customer
)
# Register your models here.
admin.site.register(Buyer)
admin.site.register(Shop)
admin.site.register(PricesType)
admin.site.register(Price)
admin.site.register(Order)
admin.site.register(OrdersProduct)
admin.site.register(Product)
admin.site.register(Customer)
