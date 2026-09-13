from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models import Veiculo, Cliente
from app.forms import RegistoForm, LoginForm
from datetime import date
from app.models import Veiculo, Cliente, Reserva, FormaPagamento
from app.forms import RegistoForm, LoginForm, ReservaForm
from app.forms import RegistoForm, LoginForm, ReservaForm, EditarReservaForm


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/pesquisa')
def pesquisa():
    # Parâmetros vindos do formulário (GET) — todos opcionais
    categoria = request.args.get('categoria')
    transmissao = request.args.get('transmissao')
    tipo = request.args.get('tipo')
    valor_max = request.args.get('valor_max', type=float)
    pessoas = request.args.get('pessoas')  # '1-4', '5-6' ou '7+'

    query = Veiculo.query

    if categoria:
        query = query.filter_by(categoria=categoria)
    if transmissao:
        query = query.filter_by(transmissao=transmissao)
    if tipo:
        query = query.filter_by(tipo=tipo)
    if valor_max is not None:
        query = query.filter(Veiculo.valor_diaria <= valor_max)

    if pessoas == '1-4':
        query = query.filter(Veiculo.quantidade_pessoas.between(1, 4))
    elif pessoas == '5-6':
        query = query.filter(Veiculo.quantidade_pessoas.between(5, 6))
    elif pessoas == '7+':
        query = query.filter(Veiculo.quantidade_pessoas >= 7)

    todos_os_resultados = query.all()

    # Excluir veículos com revisão/inspeção fora do prazo (nunca alugáveis, independentemente da data)
    veiculos = [v for v in todos_os_resultados if v.esta_valido()]

    filtros_aplicados = {
        'categoria': categoria,
        'transmissao': transmissao,
        'tipo': tipo,
        'valor_max': valor_max,
        'pessoas': pessoas,
    }

    return render_template('resultados.html', veiculos=veiculos, filtros=filtros_aplicados)

@main.route('/registo', methods=['GET', 'POST'])
def registo():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistoForm()
    if form.validate_on_submit():
        email_existente = Cliente.query.filter_by(email=form.email.data).first()
        if email_existente:
            flash('Já existe uma conta com este email.', 'danger')
            return redirect(url_for('main.registo'))

        novo_cliente = Cliente(
            nome=form.nome.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(novo_cliente)
        db.session.commit()

        flash('Conta criada com sucesso! Já podes entrar.', 'success')
        return redirect(url_for('main.login'))

    return render_template('registo.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(email=form.email.data).first()

        if cliente and check_password_hash(cliente.password_hash, form.password.data):
            login_user(cliente)
            flash('Sessão iniciada com sucesso.', 'success')
            return redirect(url_for('main.index'))

        flash('Email ou palavra-passe incorretos.', 'danger')

    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    flask_login.flask_login.logout_user()
    flash('Sessão terminada.', 'success')
    return redirect(url_for('main.index'))

def veiculo_disponivel_no_periodo(veiculo_id, data_inicio, data_fim, ignorar_reserva_id=None):
    """Verifica se não há sobreposição com nenhuma reserva ativa desse veículo nesse período."""
    query = Reserva.query.filter(
        Reserva.veiculo_id == veiculo_id,
        Reserva.estado == 'ativa',
        Reserva.data_inicio <= data_fim.isoformat(),
        Reserva.data_fim >= data_inicio.isoformat()
    )
    if ignorar_reserva_id:
        query = query.filter(Reserva.id != ignorar_reserva_id)

    return query.first() is None


@main.route('/reservar/<int:veiculo_id>', methods=['GET', 'POST'])
@login_required
def reservar(veiculo_id):
    veiculo = Veiculo.query.get_or_404(veiculo_id)

    if not veiculo.esta_valido():
        flash('Este veículo não está disponível para reserva (revisão ou inspeção fora do prazo).', 'danger')
        return redirect(url_for('main.index'))

    form = ReservaForm()
    form.forma_pagamento_id.choices = [(fp.id, fp.nome) for fp in FormaPagamento.query.all()]

    if form.validate_on_submit():
        data_inicio = form.data_inicio.data
        data_fim = form.data_fim.data

        if data_fim < data_inicio:
            flash('A data de fim não pode ser anterior à data de início.', 'danger')
            return render_template('reserva.html', form=form, veiculo=veiculo)

        if data_inicio < date.today():
            flash('A data de início não pode ser no passado.', 'danger')
            return render_template('reserva.html', form=form, veiculo=veiculo)

        if not veiculo_disponivel_no_periodo(veiculo.id, data_inicio, data_fim):
            flash('Este veículo já está reservado nesse período. Escolhe outras datas.', 'danger')
            return render_template('reserva.html', form=form, veiculo=veiculo)

        num_dias = (data_fim - data_inicio).days + 1  # inclui o dia de início e o de fim
        valor_total = round(veiculo.valor_diaria * num_dias, 2)

        nova_reserva = Reserva(
            cliente_id=current_user.id,
            veiculo_id=veiculo.id,
            data_inicio=data_inicio.isoformat(),
            data_fim=data_fim.isoformat(),
            valor_total=valor_total,
            forma_pagamento_id=form.forma_pagamento_id.data,
            estado='ativa'
        )
        db.session.add(nova_reserva)
        db.session.commit()

        flash('Reserva confirmada com sucesso! Valor total: {:.2f} €'.format(valor_total), 'success')
        return redirect(url_for('main.index'))

    return render_template('reserva.html', form=form, veiculo=veiculo)

@main.route('/minhas-reservas')
@login_required
def minhas_reservas():
    reservas = Reserva.query.filter_by(cliente_id=current_user.id).order_by(Reserva.data_inicio.desc()).all()
    return render_template('minhas_reservas.html', reservas=reservas)


@main.route('/reserva/<int:reserva_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)

    # Segurança: só o dono da reserva pode editá-la
    if reserva.cliente_id != current_user.id:
        flash('Não tens permissão para editar esta reserva.', 'danger')
        return redirect(url_for('main.minhas_reservas'))

    if reserva.estado != 'ativa':
        flash('Esta reserva já está cancelada e não pode ser editada.', 'danger')
        return redirect(url_for('main.minhas_reservas'))

    form = EditarReservaForm()

    if request.method == 'GET':
        form.data_inicio.data = date.fromisoformat(reserva.data_inicio)
        form.data_fim.data = date.fromisoformat(reserva.data_fim)

    if form.validate_on_submit():
        data_inicio = form.data_inicio.data
        data_fim = form.data_fim.data

        if data_fim < data_inicio:
            flash('A data de fim não pode ser anterior à data de início.', 'danger')
            return render_template('editar_reserva.html', form=form, reserva=reserva)

        if data_inicio < date.today():
            flash('A data de início não pode ser no passado.', 'danger')
            return render_template('editar_reserva.html', form=form, reserva=reserva)

        # Exclui a própria reserva da verificação de sobreposição
        if not veiculo_disponivel_no_periodo(reserva.veiculo_id, data_inicio, data_fim,
                                              ignorar_reserva_id=reserva.id):
            flash('O veículo já está reservado nesse período. Escolhe outras datas.', 'danger')
            return render_template('editar_reserva.html', form=form, reserva=reserva)

        num_dias = (data_fim - data_inicio).days + 1
        reserva.data_inicio = data_inicio.isoformat()
        reserva.data_fim = data_fim.isoformat()
        reserva.valor_total = round(reserva.veiculo.valor_diaria * num_dias, 2)

        db.session.commit()
        flash('Reserva atualizada com sucesso.', 'success')
        return redirect(url_for('main.minhas_reservas'))

    return render_template('editar_reserva.html', form=form, reserva=reserva)


@main.route('/reserva/<int:reserva_id>/cancelar', methods=['POST'])
@login_required
def cancelar_reserva(reserva_id):
    reserva = Reserva.query.get_or_404(reserva_id)

    if reserva.cliente_id != current_user.id:
        flash('Não tens permissão para cancelar esta reserva.', 'danger')
        return redirect(url_for('main.minhas_reservas'))

    reserva.estado = 'cancelada'
    db.session.commit()
    flash('Reserva cancelada.', 'success')
    return redirect(url_for('main.minhas_reservas'))