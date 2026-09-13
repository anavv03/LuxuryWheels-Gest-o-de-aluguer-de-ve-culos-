from datetime import date
from app import db
from app import login_manager
from flask_login import UserMixin

class Cliente(UserMixin, db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    data_registo = db.Column(db.DateTime, server_default=db.func.now())

    reservas = db.relationship('Reserva', backref='cliente', lazy=True)


class FormaPagamento(db.Model):
    __tablename__ = 'formas_pagamento'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False, unique=True)


class Veiculo(db.Model):
    __tablename__ = 'veiculos'

    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String, nullable=False)
    modelo = db.Column(db.String, nullable=False)
    categoria = db.Column(db.String, nullable=False)       # Pequeno/Médio/Grande/SUV/Luxo
    transmissao = db.Column(db.String, nullable=False)      # Automático/Manual
    tipo = db.Column(db.String, nullable=False)             # Carro/Moto
    quantidade_pessoas = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String)
    valor_diaria = db.Column(db.Float, nullable=False)
    data_ultima_revisao = db.Column(db.String, nullable=False)   # 'YYYY-MM-DD'
    data_proxima_revisao = db.Column(db.String, nullable=False)
    data_ultima_inspecao = db.Column(db.String, nullable=False)

    reservas = db.relationship('Reserva', backref='veiculo', lazy=True)

    def esta_valido(self):
        """Verifica revisão e inspeção — sem olhar a reservas (isso é à parte, por datas)."""
        hoje = date.today()
        proxima_revisao = date.fromisoformat(self.data_proxima_revisao)
        ultima_inspecao = date.fromisoformat(self.data_ultima_inspecao)

        revisao_em_dia = proxima_revisao >= hoje
        inspecao_em_dia = (hoje - ultima_inspecao).days <= 365

        return revisao_em_dia and inspecao_em_dia


class Reserva(db.Model):
    __tablename__ = 'reservas'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'), nullable=False)
    data_inicio = db.Column(db.String, nullable=False)  # 'YYYY-MM-DD'
    data_fim = db.Column(db.String, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    forma_pagamento_id = db.Column(db.Integer, db.ForeignKey('formas_pagamento.id'), nullable=False)
    estado = db.Column(db.String, nullable=False, default='ativa')  # 'ativa' / 'cancelada'
    data_criacao = db.Column(db.DateTime, server_default=db.func.now())

    forma_pagamento = db.relationship('FormaPagamento')
    
    @login_manager.user_loader
    def load_user(user_id):
        return Cliente.query.get(int(user_id))