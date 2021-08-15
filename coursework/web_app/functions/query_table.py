from web_app.models.database import db
from sqlalchemy import (
    inspect,
    and_)

from ..models import (
    Product,        # __tablename__ = 'products'
    Role,           # __tablename__ = 'roles'
    User,           # __tablename__ = 'users'
    Order,          # __tablename__ = 'orders'
    Shop,           # __tablename__ = 'shops'
    Buyer,          # __tablename__ = 'buyers'
    Price,          # __tablename__ = 'prices'
    PricesType,     # __tablename__ = 'prices_type'
    OrdersProduct,  # __tablename__ = 'orders_products'
    Territory)

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
    'orders_products': OrdersProduct
}


class QueryTable:
    def __init__(self, table_name):
        eng = db.get_engine()
        insp = inspect(eng)
        self.model = models[table_name]
        if self.model.is_association:
            self.mod_for_query = db.metadata.tables[table_name]
            self.mod_for_filter = self.mod_for_query.c
        else:
            self.mod_for_query = self.model
            self.mod_for_filter = self.model
        self.table_col = insp.get_columns(table_name)
        self.columns = [col['name'] for col in self.table_col]
        self.foreign_keys = insp.get_foreign_keys(table_name)
        self.indexes = insp.get_indexes(table_name)
        self.primary_key = insp.get_pk_constraint(table_name)
        self.fk_cc = {fk['constrained_columns'][0]:
                           {'table': fk['referred_table'],
                            'col': fk['referred_columns'][0]} for fk in self.foreign_keys}
        self.table = db.metadata.tables[table_name]

    def query(self, st):
        filters = [(self.mod_for_filter, col, st[col]) for col in st.keys()]
        binary_expressions = [getattr(table, attribute) == value for table, attribute, value in filters]
        res = db.session.query(self.mod_for_query).filter(and_(*binary_expressions)).first()
        if self.model.is_association:
            if res is None:
                return res
            dc = {col: getattr(res, col) for col in self.columns}
            obj = self.model(**dc)
            return obj
        else:
            return res

    def fields(self, st):
        res = self.query(st)
        return [{'header': res.relation(col).header(col, obj=res), 'repr': res.relation(col).repr(col)}
                for col in filter(lambda c: (c in self.fk_cc.keys()), self.columns)] + \
               [{'header': res.header(col, res), 'repr': str(getattr(res, col))}
                for col in filter(lambda c: (c not in self.fk_cc.keys()), self.columns)]

    def add(self, form):
        if isinstance(form, dict):
            d = form
        else:
            d = {col: getattr(form, col).data for col in self.columns}
        obj = self.model(**d)
        if self.model.is_association:
            obj.add()
        else:
            db.session.add(obj)

    def delete(self, st):
        res = self.query(st)
        if self.model.is_association:
            res.delete()
        else:
            db.session.delete(res)
