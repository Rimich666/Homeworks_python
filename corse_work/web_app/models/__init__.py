from .database import db, login
from .product import (
    Product,        # __tablename__ = 'products'
    Order,          # __tablename__ = 'orders'
    Shop,           # __tablename__ = 'shops'
    territory,
    Buyer,          # __tablename__ = 'buyers'
    Price,          # __tablename__ = 'prices'
    PricesType,     # __tablename__ = 'prices_type'
    OrdersProduct,  # __tablename__ = 'orders_products'
    Territory,
    CountOrder,
    )

from .user import (
    Role,           # __tablename__ = 'roles'
    User,           # __tablename__ = 'users'
)

models = {
    'products': Product,
    'roles': Role,
    'users': User,
    'orders': Order,
    'shops': Shop,
    'territory': Territory,
    'buyers': Buyer,
    'prices': Price,
    'prices_type': PricesType,
    'orders_products': OrdersProduct,
    'count_orders': CountOrder
}