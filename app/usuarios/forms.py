from flask_wtf import FlaskForm
#from flask_uploads import UploadSet, IMAGES
from wtforms import StringField, SubmitField, BooleanField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from app.models import Usuario
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(),])
    lembrar = BooleanField('Lembrar senha')
    submit_button = SubmitField('Entrar')


class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(),  Length(min=3,max=128),])
    email = StringField('Email', validators=[DataRequired(), Email(),])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=5),])
    confirmar_senha = PasswordField('Confirmar senha', 
                                    validators=[DataRequired(), 
                                    EqualTo('senha')])
    submit_button = SubmitField('Cadastrar')

    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está cadastrado!')

#images = UploadSet('images', IMAGES)

class UpdateFoto(FlaskForm):
    foto = FileField(
        'Atualizar Foto',
        validators=[FileRequired(),
        FileAllowed(['jpg', 'png'], message='Imagens em .jpg ou .png apenas!')]
        )
    submit_button = SubmitField('Salvar')


class GetTokenForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_button = SubmitField('Recuperar senha')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is None:
            raise ValidationError('Esse email não está registrado!')


class NovaSenhaForm(FlaskForm):
    senha = PasswordField('Nova senha', validators=[DataRequired(),
                                                    Length(min=5)])
    confirmar_senha = PasswordField('Confirme a nova senha',
                                    validators=[DataRequired(),
                                    EqualTo('senha', message='Os campos devem ser iguais!')])
    submit_button = SubmitField('Criar nova senha')


class ConvidarRevisor(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit_button = SubmitField('Convidar novo revisor')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is None:
            raise ValidationError('Esse email não está registrado!')
        if usuario == current_user:
            raise ValidationError('Você já é revisor!')
        if usuario.permissao > 0:
            raise ValidationError('Usuário já é revisor!')
