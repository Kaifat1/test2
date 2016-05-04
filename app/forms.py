from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
    login = StringField('Логин', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить', default=False)
    submit = SubmitField('Вход')