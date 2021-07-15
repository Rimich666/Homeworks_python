from .database import db
from .product import (
    Product,        # __tablename__ = 'products'
    Role,           # __tablename__ = 'roles'
    User,           # __tablename__ = 'users'
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
from .query_table import (
    models,
    QueryTable
    )
from .trial_data import (
    make_test_data,
    delete_data
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

