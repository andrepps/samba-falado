from . import bp_letras
from flask import abort, redirect, url_for,render_template, flash
from app import db
from app.models import Musica, Compositor
from app.letras.forms import LetraForm
from app.utils import parseComp
from flask_login import login_required, current_user
import re

@bp_letras.route('/musicas/editar/<int:id>/', methods=['GET', 'POST'])
@login_required
def editar(id):
    musica = Musica.query.get_or_404(id)

    if current_user.permissao == 0:
        abort(403)
    
    form = LetraForm()
    
    if form.validate_on_submit():
        ## remove compositores 'antigos'
        comp = []
        for compositor in musica.compositores:
            comp.append(compositor)
        musica.compositores=[]
        for compositor in comp:
            if not compositor.musicas: ##alert
                db.session.delete(compositor)
        ## insere 'novos' compositores
        compositores = re.split('&|/|-|–|,', form.compositores.data) 
        for compositor in compositores:
            compositor = compositor.strip() 
            query_compositor = Compositor.query.filter_by(nome=compositor).first()
            if not query_compositor:
                novo_compositor = Compositor(nome=compositor)
                db.session.add(novo_compositor)
                musica.compositores.append(novo_compositor)
            else: 
                musica.compositores.append(query_compositor)
        ## atualiza os demais dados
        musica.nome = form.nome.data
        musica.letra = form.letra.data
        musica.informacoes = form.informacoes.data
        db.session.commit()

        flash(f'Editado com sucesso!', 'success')
        return redirect(url_for('bp_letras.letra', id=musica.id))
    form.nome.data = musica.nome
    form.compositores.data  = parseComp(musica.compositores)
    form.letra.data = musica.letra
    form.informacoes.data = musica.informacoes
    return render_template('letras/letra_form.html', form=form, legend='Editar Letra')



