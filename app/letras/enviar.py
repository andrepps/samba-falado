
from . import bp_letras
from flask import flash, redirect, url_for, render_template
from app import db
from app.models import Musica, Compositor, EmRevisao
from app.letras.forms import LetraForm
from flask_login import current_user, login_required
import re

@bp_letras.route('/letras/enviar/', methods=['POST', 'GET'])
@login_required
def enviar():
    form = LetraForm()
    if form.validate_on_submit():
        if current_user.permissao > 0:
            nova_musica = Musica(nome=form.nome.data, 
                        letra=form.letra.data, 
                        enviado_por=current_user,
                        informacoes=form.informacoes.data)
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
            db.session.commit()
            
            flash(f'Letra enviada com sucesso!', 'success')
        else:
            nova_musica = EmRevisao(nome=form.nome.data,
                                    compositores=form.compositores.data,
                                    letra=form.letra.data,
                                    enviado_por=current_user,
                                    informacoes=form.informacoes.data)
            db.session.add(nova_musica)
            db.session.commit()
            flash(f'A letra que você enviou passará por um processo de revisão e em breve será publicada. Obrigado!', 'info')
        return redirect(url_for('bp_main.main'))
    return render_template('letras/letra_form.html', form=form, legend='Enviar Letra')






    

