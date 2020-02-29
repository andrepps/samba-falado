from . import bp_usuarios

from flask import render_template, url_for, flash, current_app
from app.usuarios.forms import UpdateFoto
from app import db
from flask_login import current_user, login_required
import os
from app.utils import save_pic
from app.models import Musica, EmRevisao
from sqlalchemy import desc



@bp_usuarios.route('/perfil/', methods=['GET', 'POST'])
@login_required
def perfil():
    form=UpdateFoto()
    if form.foto.errors:
        print(form.foto.errors)
        for error in form.foto.errors:
            flash(error, 'danger')
    if form.validate_on_submit():
        if current_user.foto != 'default.png' :           
            os.remove(os.path.join(current_app.root_path, 
                                    'static/images/profile_pics', 
                                    current_user.foto))
        current_user.foto = save_pic(form.foto.data)
        db.session.commit()

    foto = url_for('static', filename='images/profile_pics/' + current_user.foto)
    letra_enviadas = current_user.letras_enviadas.order_by(desc(Musica.enviado_em))
    letras_em_revisao = current_user.letras_em_revisao.order_by(desc(EmRevisao.enviado_em))
    return render_template('usuarios/perfil.html', foto=foto, form=form, em_revisao=letras_em_revisao, enviadas=letra_enviadas) 



