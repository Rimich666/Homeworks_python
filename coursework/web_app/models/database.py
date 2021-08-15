from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from web_app.forms.admin_forms import *

db = SQLAlchemy()
login = LoginManager()


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