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

    @property
    def hpassword(self):
        return self.hpassword

    @hpassword.setter
    def hpassword(self, v):
        raise PermissionError("Nao pode mexer na hash")

    def delete_all(self):
       with SessionLocal() as session:
           users = session.query(Users).all()
           for user in users:
              session.delete(user)
              session.commit()

    def select_data(self, email: str) -> SessionLocal():
        with SessionLocal() as session:
             users = session.query(Users).filter(Users.email==email).first()
             return users

    def select_all(self):
        with SessionLocal() as session:
            users = session.query(Users).all()
            for c in users:
                dados.append()

    def insert(self, nome: str, snome: str, email: str, hpassword: str):
        with SessionLocal() as session:
             u = Users(nome=nome, snome=snome, email=email, hpassword=hpassword)
             session.add(u)
             session.commit()

BClass.metadata.create_all(motor)




