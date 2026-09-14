# Luxury Wheels

Aplicação web para aluguer de veículos (carros e motas), desenvolvida em Flask, com registo e autenticação de clientes, pesquisa de veículos com filtros, sistema de reservas com cálculo automático de valor e um painel de administração para gestão do catálogo de veículos.

## Funcionalidades

### Clientes
- Registo de conta e autenticação (passwords guardadas com hash, nunca em texto simples).
- Pesquisa de veículos com filtros por categoria, transmissão, tipo, valor máximo da diária e quantidade de pessoas.
- Veículos com revisão ou inspeção obrigatória fora do prazo são automaticamente excluídos dos resultados.
- Reserva de um veículo escolhendo data de início, data de fim e forma de pagamento.
- Cálculo automático do valor total da reserva (valor da diária × número de dias).
- Verificação de disponibilidade: um veículo só fica indisponível durante o período de datas já reservado (sem sobreposição).
- Página "As Minhas Reservas", com possibilidade de editar as datas de uma reserva ativa ou cancelá-la por completo.

### Administrador
- Painel de gestão de veículos, acessível apenas a contas com permissão de administrador.
- Adicionar, editar e eliminar veículos do catálogo.
- Upload de imagem do veículo a partir do computador (em vez de introduzir uma URL).
- Não é possível eliminar um veículo que já tenha reservas associadas, para preservar o histórico.

## Tecnologias utilizadas

- **Python 3** com **Flask**
- **Flask-SQLAlchemy** — ORM e gestão da base de dados
- **Flask-Login** — autenticação e gestão de sessão
- **Flask-WTF** — formulários e proteção CSRF
- **SQLite** — base de dados (gerida também via DB Browser for SQLite)
- **Bootstrap 5** — interface visual
- **Jinja2** — motor de templates

## Estrutura do projeto

LuxuryWheels/
├── app/
│ ├── init.py # criação e configuração da app Flask
│ ├── models.py # modelos da base de dados (Cliente, Veiculo, Reserva, FormaPagamento)
│ ├── routes.py # rotas da aplicação
│ ├── forms.py # formulários (registo, login, reserva, veículo)
│ ├── static/
│ │ ├── css/
│ │ └── imagens/ # imagens dos veículos (upload pelo administrador)
│ └── templates/ # templates HTML (Jinja2)
├── database/
│ └── luxury_wheels.db # base de dados SQLite
├── config.py # configurações da aplicação
├── run.py # ponto de entrada da aplicação
└── requirements.txt # dependências do projeto


## Modelo de dados

- **Cliente**: nome, email, password (hash), data de registo, indicador de administrador.
- **Veiculo**: marca, modelo, categoria, transmissão, tipo, quantidade de pessoas, imagem, valor da diária, data da última revisão, data da próxima revisão, data da última inspeção obrigatória.
- **Reserva**: cliente, veículo, data de início, data de fim, valor total, forma de pagamento, estado (ativa/cancelada).
- **FormaPagamento**: catálogo de formas de pagamento disponíveis.

Um veículo é considerado disponível para reserva quando:
1. A data da próxima revisão ainda não passou.
2. A data da última inspeção obrigatória não tem mais de 1 ano.
3. Não existe nenhuma reserva ativa desse veículo com datas sobrepostas ao período pedido.

## Como correr o projeto localmente

1. Clonar o repositório e entrar na pasta do projeto:
```bash
   git clone <URL_DO_REPOSITORIO>
   cd LuxuryWheels
```

2. Criar e ativar o ambiente virtual:
```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Mac / Linux
   source venv/bin/activate
```

3. Instalar as dependências:
```bash
   pip install -r requirements.txt
```

4. Garantir que existe a base de dados em `database/luxury_wheels.db`, com as tabelas criadas (ver secção "Base de dados" abaixo).

5. Correr a aplicação:
```bash
   python run.py
```

6. Abrir no browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Base de dados

A base de dados é criada e gerida através do **DB Browser for SQLite**. O esquema das tabelas encontra-se documentado nos comentários de `app/models.py`, e pode ser recriado executando os `CREATE TABLE` correspondentes na aba **Execute SQL** do DB Browser.

Para criar uma conta de administrador, atualizar diretamente a coluna `is_admin` do cliente pretendido:

```sql
UPDATE clientes SET is_admin = 1 WHERE email = 'email-do-administrador@exemplo.com';
```

## Autor

Projeto desenvolvido por Ana Venâncio, no âmbito do módulo de desenvolvimento web da Tokio School.