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
    buyer = StringField('Покупатель', validators=[DataRequired()])
    shop = StringField('Магазин', validators=[DataRequired()])
    buyer_id = IntegerField('', validators=[DataRequired()])
    shop_id = IntegerField('', validators=[DataRequired()])
    submit = SubmitField('Записать')

    pass


class ProdField(DecimalField):
    validators = [DataRequired()]
    places = 3
    label = 'Количество'

    def __init__(self, id, **kwargs):
        super().__init__(**kwargs)
        self.id =id


class Row:
    def __init__(self, val, prc, prd, sum, nm):
        self.val = val
        self.price_val = prc
        self.prod = prd
        self.sum = sum
        self.name = nm