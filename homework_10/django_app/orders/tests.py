from django.test import TestCase
from .functions import (
    create_random_order,
    create_trial_data,
    delete_all)
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


# Create your tests here.


class TestOrder(TestCase):
    def setUp(self):
        create_trial_data()

    def tearDown(self):
        delete_all()

    def test_create(self):
        self.assertTrue(len(Buyer.objects.all()) > 0)
        self.assertTrue(len(Shop.objects.all()) > 0)
        self.assertTrue(len(PricesType.objects.all()) > 0)
        self.assertTrue(len(Price.objects.all()) > 0)
        self.assertTrue(len(Order.objects.all()) > 0)
        self.assertTrue(len(OrdersProduct.objects.all()) > 0)
        self.assertTrue(len(Product.objects.all()) > 0)
        self.assertTrue(len(Customer.objects.all()) > 0)

    def test_create_order(self):
        order = create_random_order()
        self.assertTrue(order in Order.objects.all())

    def test_views(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/orders/list')
        self.assertEqual(response.status_code, 200)
        for order in Order.objects.all():
            str_get = '/orders/detail/' + str(order.id)
            response = self.client.get(str_get)
            self.assertEqual(response.status_code, 200)

    def test_content(self):
        response = self.client.get('/orders/list')
        for order in Order.objects.all():
            b_num = order.num.encode(encoding='utf-8')
            self.assertIn(b_num, response.content)
        for order in Order.objects.all():
            response = self.client.get('/orders/detail/' + str(order.id))
            b_num = order.buyer.buyer_name.encode(encoding='utf-8')
            self.assertIn(b_num, response.content)
    pass
