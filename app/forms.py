from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField('Título', [DataRequired('Este campo es obligatorio.')])
    body = TextAreaField('Cuerpo', [DataRequired('Este campo es obligatorio.')])
    submit = SubmitField('Publicar')


class EditPostForm(FlaskForm):
    title = StringField('Título', [DataRequired('Este campo es obligatorio.')])
    body = TextAreaField('Cuerpo', [DataRequired('Este campo es obligatorio.')])
    submit = SubmitField('Editar')