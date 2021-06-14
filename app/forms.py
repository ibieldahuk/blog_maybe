from wtforms import Form, StringField, TextAreaField, SubmitField


class CreatePostForm(Form):
    title = StringField('Título')
    body = TextAreaField('Cuerpo')
    submit = SubmitField('Publicar')


class EditPostForm(Form):
    title = StringField('Título')
    body = TextAreaField('Cuerpo')
    submit = SubmitField('Editar')