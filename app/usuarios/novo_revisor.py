from . import bp_usuarios
from .forms import ConvidarRevisor
from flask import render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Usuario
from app.utils import avisar_novo_revisor
from app import db



@bp_usuarios.route('/novo-revisor/', methods=['GET', 'POST'])
@login_required
def convidar_revisor():
    if current_user.permissao < 2:
        abort(403)
    form = ConvidarRevisor()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        usuario.permissao = 1
        print(usuario.email)
        db.session.commit()
        avisar_novo_revisor(usuario)
        return redirect(url_for('bp_usuarios.perfil'))
    return render_template('usuarios/convidar_revisor.html', form=form)
