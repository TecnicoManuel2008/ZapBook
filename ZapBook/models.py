from sqlalchemy.orm import declarative_base, sessionmaker
from flask_login import UserMixin
import sqlalchemy as db

motor = db.create_engine("sqlite:///users.db")
SessionLocal = sessionmaker(bind=motor)
BClass = declarative_base()

class Users(BClass, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(50), nullable=False)
    snome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    hpassword = db.Column(db.String(200), nullable=False)

BClass.metadata.create_all(motor)
