from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    UniqueConstraint
)
from sqlalchemy.orm import (relationship)

from .database import db
from forms import *


class Templ:
    add_form = AddDefault
    add_templ = 'add_default'
    repr_templ = ''
    many_to_many = False
    headers = {'default': 'Заголовок не задан'}
    relations = {}
    is_association = False

    def header(self, col, obj):
        if col in self.headers.keys():
            return self.headers[col]
        else:
            if obj == self:
                return col
            else:
                return self.headers['default']

    def repr(self, col=''):
        return getattr(self, col)

    def relation(self, col):
        if col in self.relations.keys():
            return getattr(self, self.relations[col])
        else:
            return self


territory = db.Table('territory',
                     Column('user_id', ForeignKey('users.id'), nullable=False),
                     Column('shop_id', ForeignKey('shops.id'), nullable=False), )


class Territory(Templ):
    is_association = True
    add_to = 'user_id'
    ref = 'shops'
    added = 'shop_id'

    def __init__(self, user_id, shop_id):
        self.user_id = user_id
        self.shop_id = shop_id
        self.user = User.query.filter_by(id=user_id).first()
        self.shop = Shop.query.filter_by(id=shop_id).first()

    def add(self):
        self.user.shops.append(self.shop)

    def delete(self):
        self.user.shops.remove(self.shop)

    def __repr__(self):
        return f'<Territory user_id = {self.user_id}, shop_id = {self.shop_id}>'


class Role(db.Model, Templ):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role = Column(String(10), unique=True, nullable=False)
    users = relationship('User', back_populates='role')

    def __init__(self, id, role):
        self.id = id
        self.role = role

    pass


class User(db.Model, Templ):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id, ondelete='CASCADE'))
    phone_number = Column(String(12), unique=False)
    role = relationship('Role', back_populates='users')
    orders = relationship('Order', back_populates='user')

    def __init__(self, id, username, role_id, phone_number):
        self.id = id
        self.username = username
        self.role_id = role_id
        self.phone_number = phone_number

    pass


class Buyer(db.Model, Templ):
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    kode = Column(Integer, unique=True, nullable=False)
    buyer_name = Column(String(100), nullable=False)
    shops = relationship('Shop', back_populates='buyer')
    orders = relationship('Order', back_populates='buyer')

    def __init__(self, id, kode, buyer_name):
        self.id = id
        self.kode = kode
        self.buyer_name = buyer_name

    pass


class Shop(db.Model, Templ):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)
    kode = Column(String(8), nullable=False)
    shop_name = Column(String(100), nullable=False)
    address = Column(String(255))

    buyer_id = Column(Integer, ForeignKey('buyers.id', ondelete='CASCADE'))
    pt_id = Column(Integer, ForeignKey('prices_type.id', ondelete='CASCADE'))

    prices_type = relationship('PricesType', back_populates='shop')
    buyer = relationship('Buyer', back_populates='shops')
    users = relationship('User', secondary=territory, backref=db.backref('shops'))
    orders = relationship('Order', back_populates='shop')

    UniqueConstraint(buyer_id, kode)

    def __init__(self, id, kode, shop_name, address, buyer_id, pt_id):
        self.id = id
        self.kode = kode
        self.shop_name = shop_name
        self.address = address
        self.buyer_id = buyer_id
        self.pt_id = pt_id

    pass


class PricesType(db.Model, Templ):
    __tablename__ = 'prices_type'
    id = Column(Integer, primary_key=True)
    pt_name = Column(String(50), unique=True, nullable=False)
    shop = relationship('Shop', back_populates='prices_type')

    headers = {'pt_name': 'Тип цены', 'default': 'Тип цены'}

    def repr(self, col=''):
        return self.pt_name

    def __init__(self, id, pt_name):
        self.id = id
        self.pt_name = pt_name

    pass


class Price(db.Model, Templ):
    __tablename__ = 'prices'
    #    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    pt_id = Column(Integer, ForeignKey('prices_type.id', ondelete='CASCADE'), nullable=False)
    price = Column(Numeric(15, 2))
    PrimaryKeyConstraint(product_id, pt_id, date, name='price_pk')
    product = relationship('Product', back_populates='prices')
    price_type = relationship('PricesType')

    relations = {'product_id': 'product', 'pt_id': 'price_type'}

    headers = {'date': 'Дата установки', 'price': 'Цена'}

    def __init__(self, product_id, date, pt_id, price):
        self.product_id = product_id
        self.date = date
        self.pt_id = pt_id
        self.price = price

    pass


class Order(db.Model, Templ):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    num = Column(String(11))
    guid = Column(String(36), unique=True)
    date = Column(DateTime)
    sum = Column(Numeric(15, 2))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    buyer_id = Column(Integer, ForeignKey('buyers.id', ondelete='CASCADE'))
    shop_id = Column(Integer, ForeignKey('shops.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='orders')
    buyer = relationship('Buyer', back_populates='orders')
    shop = relationship('Shop', back_populates='orders')
    orders_products = relationship('OrdersProduct', back_populates='order')

    def __init__(self, id, num, guid, date, sum, user_id, buyer_id, shop_id):
        self.id = id
        self.num = num
        self.guid = guid
        self.date = date
        self.sum = sum
        self.user_id = user_id
        self.buyer_id = buyer_id
        self.shop_id = shop_id

    pass


class OrdersProduct(db.Model, Templ):
    __tablename__ = 'orders_products'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id', ondelete='CASCADE'))
    product_id = Column(Integer, ForeignKey('products.id', ondelete='CASCADE'))
    quantity = Column(Numeric(14, 3), nullable=False)
    sum = Column(Numeric(15, 2), nullable=False)
    price = Column(Numeric(15, 2), nullable=False)
    order = relationship('Order', back_populates='orders_products')
    product = relationship('Product', back_populates='order_products')

    def __init__(self, id, order_id, product_id, quantity, sum, price):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.sum = sum
        self.price = price

    pass


class Product(db.Model, Templ):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(100), nullable=False, unique=True)
    kode = Column(Integer, unique=True, nullable=False)
    order_products = relationship('OrdersProduct', back_populates='product')
    prices = relationship('Price', back_populates='product')

    headers = {'default': "Товар", 'product_name': 'Наименование'}

    def repr(self, col=''):
        return self.product_name

    def __init__(self, id, product_name, kode):
        self.id = id
        self.product_name = product_name
        self.kode = kode

    pass


if __name__ == '__main__':
    pass
