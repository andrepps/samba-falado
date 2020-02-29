from . import bp_usuarios

from flask import flash, render_template, redirect, url_for
from app.usuarios.forms import GetTokenForm, NovaSenhaForm
from app.models import Usuario
from app import db, bcrypt
from flask_login import current_user
from app.utils import enviar_token


@bp_usuarios.route('/recuperar-senha/', methods=['GET', 'POST'])
def get_token():
    if current_user.is_authenticated:
        return redirect(url_for('bp_main.main'))
    form = GetTokenForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        enviar_token(usuario)
        flash('Confirme seu email para criar uma nova senha!', 'info')
        return redirect(url_for('bp_usuarios.login'))
    return render_template('usuarios/recuperar_senha.html', form=form)

@bp_usuarios.route('/recuperar-senha/<token>/', methods=['GET', 'POST'])
def nova_senha(token):
    if current_user.is_authenticated:
        return redirect(url_for('bp_main.main'))
    usuario = Usuario.verify_token(token)
    if usuario is None:
        flash('Requsição invalida ou expirada', 'warning')
        return redirect(url_for('bp_usuarios.get_token'))
    form = NovaSenhaForm()
    if form.validate_on_submit():
        senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        usuario.senha = senha_hash
        db.session.commit()
        flash('Senha atualizada!', 'success')
        return redirect(url_for('bp_usuarios.login'))
    return render_template('usuarios/nova_senha.html', form=form)