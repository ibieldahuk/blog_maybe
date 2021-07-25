from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class CreatePostForm(FlaskForm):
    title = StringField('Título', [DataRequired('Este campo es obligatorio.')])
    body = TextAreaField('Cuerpo', [DataRequired('Este campo es obligatorio.')])
    submit = SubmitField('Publicar')


class EditPostForm(FlaskForm):
    title = StringField('Título', [DataRequired('Este campo es obligatorio.')])
    body = TextAreaField('Cuerpo', [DataRequired('Este campo es obligatorio.')])
    submit = SubmitField('Editar')


class UserLoginForm(FlaskForm):
    username = StringField('Nombre de usuario', [DataRequired('Este campo es obligatorio.')])
    email = StringField('Dirección de correo electrónico', [DataRequired('Este campo es obligatorio.'), Email()])
    password = PasswordField('Contraseña', [DataRequired('Este campo es obligatorio.')])
    remember_me = BooleanField('Recordar cuenta.')
    submit = SubmitField('Ingresar')


class UserRegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', [DataRequired('Este campo es obligatorio.')])
    email = StringField('Dirección de correo electrónico', [DataRequired('Este campo es obligatorio.'), Email()])
    password = PasswordField('Contraseña', [DataRequired('Este campo es obligatorio.')])
    password2 = PasswordField('Repita la contraseña', [DataRequired('Este campo es obligatorio'), EqualTo('password')])
    submit = SubmitField('Crear cuenta')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Este nombre de usuario ya está siendo utilizado.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Esta dirección de correo electrónico ya está siendo utilizada.')
