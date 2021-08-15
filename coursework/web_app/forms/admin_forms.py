from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DecimalField,
    DateTimeField,
    SubmitField,
    HiddenField
)
from wtforms.widgets import TextInput
from wtforms.widgets.html5 import (
    NumberInput,
    DateTimeInput,

)
from wtforms.validators import InputRequired

types_field = {'VARCHAR': {'ftype': StringField, 'widget': TextInput()},
               'INTEGER': {'ftype': IntegerField, 'widget': NumberInput()},
               'NUMERIC': {'ftype': DecimalField, 'widget': NumberInput()},
               'TIMESTAMP': {'ftype': DateTimeField, 'widget': DateTimeInput()},
               'DATETIME': {'ftype': DateTimeField, 'widget': DateTimeInput()}}


def create_add_form(Class):
    def create_form(columns):
        field_list = Class.field_list
        print(field_list)
        for field in field_list:
            delattr(Class, field)

        field_list = []
        for col in columns:
            fieldname = col['name']
            strt = col['type'].__visit_name__
            setattr(Class, fieldname,
                    types_field[strt]['ftype'](fieldname.capitalize(), validators=[InputRequired()],
                                               widget=types_field[strt]['widget']))
            field_list.append(fieldname)
            setattr(Class, 'List', StringField(str(field_list)))
        Class.field_list = field_list
        form = Class()
        return form

    return create_form


@create_add_form
class AddDefault(FlaskForm):
    #field_list = HiddenField(None)
    field_list = []
    # def __init__(self, field_list):
    #     self.field_list = ",".join(field_list)

    pass