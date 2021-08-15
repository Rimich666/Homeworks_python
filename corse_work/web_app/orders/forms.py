from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DecimalField,
    DateTimeField,
    SubmitField,
    HiddenField
)

from wtforms.validators import DataRequired


class Val:
    pass


class AddOrderForm(FlaskForm, Val):
    submit = SubmitField('Записать')

    pass


class Row:
    def __init__(self, val, prc, prd, sum, nm):
        self.val = val
        self.price_val = prc
        self.prod = prd
        self.sum = sum
        self.name = nm

    def __str__(self):
        return f" {self.prod.id} {self.prod.product_name}: {self.val}"
