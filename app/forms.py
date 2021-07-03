from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class CreatePostForm(FlaskForm):
    title = StringField('Título', [DataRequired('Complete este campoOoOo.')])
    body = TextAreaField('Cuerpo', [DataRequired('Complete este campoOoOo.')])
    submit = SubmitField('Publicar')


class EditPostForm(FlaskForm):
    title = StringField('Título', [DataRequired('Complete este campoOoOo.')])
    body = TextAreaField('Cuerpo', [DataRequired('Complete este campoOoOo.')])
    submit = SubmitField('Editar')