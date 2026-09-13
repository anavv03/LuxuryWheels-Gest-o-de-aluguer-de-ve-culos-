from app import create_app, db
from app.models import Veiculo

app = create_app()
with app.app_context():
    for v in Veiculo.query.all():
        print(v.marca, v.modelo, v.esta_valido())