from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    ValidationError,
    EqualTo
)
from ..models import User
from wtforms.widgets.html5 import (
    NumberInput
)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    send_sms = BooleanField('Хочу СМСку')
    submit = SubmitField('Sign In')


class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = IntegerField('Role', validators=[DataRequired()])

#    role = SelectField('Role', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')


class ConfirmForm(FlaskForm):
    code = IntegerField('Code', validators=[DataRequired(), InputRequired()], widget=NumberInput())
    submit = SubmitField('Подтвердить')
