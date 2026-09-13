import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'muda-isto-para-uma-chave-secreta-tua'  # usada pelo Flask para sessões/formulários
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'luxury_wheels.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # desativa um aviso desnecessário do SQLAlchemy