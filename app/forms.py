import flask_wtf
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegistoForm(flask_wtf.FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Palavra-passe', validators=[DataRequired(), Length(min=6)])
    confirmar_password = PasswordField(
        'Confirmar palavra-passe',
        validators=[DataRequired(), EqualTo('password', message='As palavras-passe não coincidem')]
    )
    submit = SubmitField('Registar')


class LoginForm(flask_wtf.FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Palavra-passe', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class ReservaForm(flask_wtf.FlaskForm):
    data_inicio = DateField('Data de início', validators=[DataRequired()], format='%Y-%m-%d')
    data_fim = DateField('Data de fim', validators=[DataRequired()], format='%Y-%m-%d')
    forma_pagamento_id = SelectField('Forma de pagamento', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Confirmar Reserva')


class EditarReservaForm(flask_wtf.FlaskForm):
    data_inicio = DateField('Data de início', validators=[DataRequired()], format='%Y-%m-%d')
    data_fim = DateField('Data de fim', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Atualizar Reserva')