
from flask import Flask, flash ,render_template, request, url_for, redirect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from models import Users, SessionLocal
from config import DevConfig
from forma import RegisterForm, LoginForm

from sqlalchemy.exc import IntegrityError
from datetime import datetime

from dotenv import load_dotenv

app = Flask(__name__)
app.config.from_object(DevConfig)

login = LoginManager(app)

login.init_app(app)
login.login_view = "main"

load_dotenv()

def get_tempo():
    hoje = f"{datetime.today().day}/{datetime.today().month}/{datetime.today().year}"
    return hoje

@login.user_loader
def cadastro(id_user):
    """ esta funcao serve de API entre
        o flask-login e o cookie
        id_user: <- id do usuario no cookie
    """
    with SessionLocal() as session:
        return session.get(Users, int(id_user))

@login.unauthorized_handler
def Unauthenticad():
    # esta funcao vai mandar o flash se o nao esta logado
    flash('Inicie Sessao ou faça login! ', 'erro')
    return redirect(url_for('main'))

@app.errorhandler(404)
def NotFound(e):
    return render_template('404.html')

@app.route('/', methods=['GET', "POST"])
def main():
    form = LoginForm() # objeto do formulario da entrada
    reponse: str = "" # respostas da execucao
    tempo = get_tempo() # dia atual
    # verificar se o usuario esta logado no cookie
    if current_user.is_authenticated:
       return redirect(url_for('perfil'))

    # se passar da validacao do formulario
    if form.validate_on_submit():
       email = form.email.data
       password = form.password.data

       with SessionLocal() as session:

          user = session.query(Users).filter(Users.email==email).first()
          if user and user != None:
             if check_password_hash(user.hpassword, password):
                login_user(user, remember=True)
                return redirect(url_for('perfil'))
             else:
                reponse = "Senha invalida"
          else:
             reponse = "Email invalido ou Email nao encotrado"

    return render_template('Signin.html', form=form, time=tempo, reponse=reponse)

@app.route('/login', methods=['GET', 'POST'])
def cadastrar():
    form = RegisterForm()
    hoje = get_tempo()
    if form.validate_on_submit():
       nome = form.name.data
       snome = form.SName.data
       email = form.email.data
       password = form.password.data

       with SessionLocal() as session:
            hpass = generate_password_hash(password)
            try:
                user = Users(nome=nome, snome=snome, email=email, hpassword=hpass)

                session.add(user)
                session.commit()
                login_user(user, remember=True)
                return redirect(url_for('perfil'))

            except IntegrityError:
                session.rollback()
                flash('Esse email ja existe!', 'info')
                return render_template('index.html', time=hoje, form=form)

    return render_template('index.html', form=form, time=hoje)

@app.route('/perfil', methods=['GET'])   
@login_required
def perfil():
    hoje = get_tempo()
    return render_template('perfil.html', time=hoje)

@app.route('/sair', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('main'))

if __name__ == '__main__':
   app.run(debug=True, port=8000)

