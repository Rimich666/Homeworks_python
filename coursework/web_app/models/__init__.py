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
    Templ,
    Territory,
    )
from .user import (
    Role,           # __tablename__ = 'roles'
    User,           # __tablename__ = 'users'
)


__all__ = (
    db,
    Product,
    Role,
    User,
    Order,
    Shop,
    territory,
    Buyer,
    Price,
    PricesType,
    OrdersProduct,
    Templ,
    Territory
)

