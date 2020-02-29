from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField    
from wtforms.validators import DataRequired

class LetraForm(FlaskForm):
    nome = StringField('Música', validators=[DataRequired()])
    compositores = StringField('Compositores', validators=[DataRequired()])
    letra = TextAreaField('Letra', validators=[DataRequired()])
    informacoes = TextAreaField('Informações adicionais sobre a música')
    submit_button = SubmitField('Enviar')



#criar form para editar compositor
#criar validações custom com ValidationError

#from app.models import Musica, Compositor
#from flask_wtf.file import FileField, FileRequired, FileAllowed

#from flask_uploads import UploadSet, IMAGES
#Length