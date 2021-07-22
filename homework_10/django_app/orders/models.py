from django.db import models
from django.utils.timezone import now


# Create your models here.


class Buyer(models.Model):
    kode = models.IntegerField(unique=True)
    buyer_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.buyer_name

    pass


class PricesType(models.Model):
    pt_name = models.CharField(max_length=50, unique=True, null=False)

    def __str__(self):
        return self.pt_name

    pass


class Shop(models.Model):
    kode = models.CharField(max_length=8)
    shop_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='shops')
    price_type = models.ForeignKey(PricesType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["buyer", "kode"], name="unique_buyer_shop"
            )
        ]

    def __str__(self):
        return self.shop_name

    pass


class Customer(models.Model):
    username = models.CharField(max_length=100, unique=True, null=False)
    phone_number = models.CharField(max_length=12, unique=False)
    shops = models.ManyToManyField(Shop, db_table='territory', related_name='customers')
    count = models.IntegerField(default=0)

    def number(self):
        self.count += 1
        return self.username[0].upper() + "{:010}".format(self.count)

    def __str__(self):
        return self.username

    pass


class Price(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='prices')
    date = models.DateTimeField(null=False, db_index=True)
    price_type = models.ForeignKey(PricesType, on_delete=models.CASCADE, null=False, related_name='prices')
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product", "date", "price_type"], name="unique_price_product"
            )
        ]

    def __str__(self):
        return f"date: {self.date} price: {self.price}"

    pass


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=False, unique=True)
    kode = models.IntegerField(unique=True)

    def __str__(self):
        return self.product_name

    pass


class Order(models.Model):
    num = models.CharField(max_length=11)
    guid = models.CharField(max_length=36, unique=True, null=True)
    date = models.DateTimeField(default=now)
    sum = models.DecimalField(max_digits=15, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='orders', null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, related_name='orders')

    def __str__(self):
        return f"Заказ № {self.num} от: {self.date} покупатель: {self.buyer} сумма: {self.sum}"

    pass


class OrdersProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders_products')
    quantity = models.DecimalField(max_digits=14, decimal_places=3)
    sum = models.DecimalField(max_digits=15, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    pass
