from . import bp_letras
from flask import abort, render_template, flash, redirect, url_for
from app import db
from app.models import EmRevisao, Usuario, Musica, Compositor
from app.letras.forms import LetraForm
from flask_login import current_user, login_required
import re

@bp_letras.route('/letras/revisar/')
@login_required
def em_revisao():
    if current_user.permissao == 0:
        abort(403)
    musicas = EmRevisao.query.all()
    usuarios = Usuario.query.all()
    return render_template('letras/em_revisao.html', musicas=musicas)

@bp_letras.route('/letras/revisar/<int:id>/', methods=['POST', 'GET'])
@login_required
def revisar(id):
    musica = EmRevisao.query.get(id)
    if (current_user != musica.enviado_por) and (current_user.permissao == 0):
        abort(403)
    form = LetraForm()
    if form.validate_on_submit():
        nova_musica = Musica(nome=form.nome.data, 
                            letra=form.letra.data, 
                            enviado_por=musica.enviado_por,
                            enviado_em=musica.enviado_em,
                            informacoes=form.informacoes.data)
        ## comp strip
        compositores = re.split('&|/|-|–|,', form.compositores.data) 
        for compositor in compositores:
            compositor = compositor.strip() 
            query_compositor = Compositor.query.filter_by(nome=compositor).first()
            if not query_compositor:
                novo_compositor = Compositor(nome=compositor)
                db.session.add(novo_compositor)
                nova_musica.compositores.append(novo_compositor)
            else: 
                nova_musica.compositores.append(query_compositor)
        db.session.add(nova_musica)
        db.session.delete(musica)
        db.session.commit()
        
        flash(f'Letra revisada com sucesso!', 'success')
        return redirect(url_for('bp_main.main'))
    form.nome.data = musica.nome
    form.compositores.data  = musica.compositores
    form.letra.data = musica.letra
    #if musica.info:
    form.informacoes.data = musica.informacoes
    return render_template('letras/letra_form.html', form=form, legend='Em revisão')