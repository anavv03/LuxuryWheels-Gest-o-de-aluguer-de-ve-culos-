import flask_wtf
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms import FloatField, IntegerField
from flask_wtf.file import FileField, FileAllowed

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

class VeiculoForm(flask_wtf.FlaskForm):
    marca = StringField('Marca', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    categoria = SelectField('Categoria', choices=[
        ('Pequeno', 'Pequeno'), ('Médio', 'Médio'), ('Grande', 'Grande'),
        ('SUV', 'SUV'), ('Luxo', 'Luxo')
    ], validators=[DataRequired()])
    transmissao = SelectField('Transmissão', choices=[
        ('Automático', 'Automático'), ('Manual', 'Manual')
    ], validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[
        ('Carro', 'Carro'), ('Moto', 'Moto')
    ], validators=[DataRequired()])
    quantidade_pessoas = IntegerField('Quantidade de pessoas',
                                       validators=[DataRequired(), NumberRange(min=1)])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png'], 'Apenas imagens são permitidas')])
    valor_diaria = FloatField('Valor da diária (€)', validators=[DataRequired(), NumberRange(min=0)])
    data_ultima_revisao = DateField('Data da última revisão', validators=[DataRequired()], format='%Y-%m-%d')
    data_proxima_revisao = DateField('Data da próxima revisão', validators=[DataRequired()], format='%Y-%m-%d')
    data_ultima_inspecao = DateField('Data da última inspeção obrigatória', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Guardar Veículo')    
    