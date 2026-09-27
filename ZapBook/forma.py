from flask_wtf import FlaskForm
from wtforms import (
   StringField, PasswordField,
   SubmitField, EmailField, IntegerField
)
from wtforms.validators import (
   DataRequired, EqualTo,
   Email, Length
)

class RegisterForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(message="Digite o Nome")])
    SName = StringField("Sobrenome", validators=[DataRequired()])
    email = EmailField("Email", validators=[
       DataRequired(message="Digite a Email")
      # Email(message="Tem que ter o @")
    ])
    password = PasswordField("Senha", validators=[
       DataRequired(message="Digite a senha"),
       Length(min=6, max=20)
    ])
    confirm = PasswordField("Confirmar", validators=[
        DataRequired(message="Digite a senha"),
        EqualTo("password", message="A senha tem que ser iguais ")        
    ])
    entrar = SubmitField("Entrar")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[
         DataRequired(message="Digite o email da sua conta ZapBook")
    ])
    password = PasswordField("Password", validators=[
         DataRequired(message="Digite a senha da sua conta ZapBook")
    ])
    entrar = SubmitField("Iniciar Sessao")

