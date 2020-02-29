from . import bp_letras
from flask import redirect, url_for, abort, flash
from app import db
from app.models import Musica, Compositor
from flask_login import login_required, current_user

@bp_letras.route('/musicas/apagar/<int:id>/', methods=['GET', 'POST'])
@login_required
def apagar(id):
    musica = Musica.query.get_or_404(id)

    if (current_user != musica.enviado_por) and (current_user.permissao == 0):
        #flash(f'Você não é revisor e nem foi você quem enviou a letra!', 'danger')
        abort(403)
        
    ## remove compositores 'antigos'
    comp = []
    for compositor in musica.compositores:
        comp.append(compositor)
    musica.compositores=[]
    for compositor in comp:
        if not compositor.musicas: ##alert
            db.session.delete(compositor)
    db.session.delete(musica)
    db.session.commit()
    
    flash(f'Apagado com sucesso!', 'info') #modal 
    return redirect(url_for('bp_main.main')) ##last