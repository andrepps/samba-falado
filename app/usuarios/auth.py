from . import bp_usuarios

from flask import redirect, flash, url_for, render_template, request
from app.usuarios.forms import CadastroForm, LoginForm
from app.models import Usuario
from app import db, bcrypt
from flask_login import login_user, current_user, logout_user

@bp_usuarios.route('/cadastro/', methods=['GET', 'POST'])
def cadastrar():
    if current_user.is_authenticated:
        return redirect(url_for('bp_main.main'))
    form = CadastroForm()
    if form.validate_on_submit():
        senha_hash = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        novo_usuario = Usuario(nome=form.nome.data,
                               email=form.email.data,
                               senha=senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()
        flash(f'Conta criada!', 'success')
        return redirect(url_for('bp_usuarios.entrar'))
    return render_template('usuarios/cadastro.html', form=form)

@bp_usuarios.route('/entrar/', methods=['GET', 'POST'])
def entrar():
    if current_user.is_authenticated:
        return redirect(url_for('bp_main.main'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('bp_main.main'))
        else:
            flash(f'Verifique seu email e senha', 'danger')
    return render_template('usuarios/login.html', form=form)


@bp_usuarios.route('/sair/')
def sair():
    logout_user()
    return redirect(url_for('bp_usuarios.entrar'))
