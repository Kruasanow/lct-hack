# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Пароль',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    username = StringField('Имя пользователя',
                         id='username_create',
                         validators=[DataRequired()])
    role = StringField('Роль',
                      id='role_create',
                      validators=[DataRequired()])
    password = PasswordField('Пароль',
                             id='pwd_create',
                             validators=[DataRequired()])
