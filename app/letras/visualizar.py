from . import bp_letras
from flask import render_template
from app.models import Musica
from app.utils import parseAlfabeto


@bp_letras.route('/letras/<int:id>/')
def letra(id):
    musica = Musica.query.get_or_404(id)
    return render_template('letras/letra.html', musica=musica)


@bp_letras.route('/letras/')
def letras():
    alfabeto = {}
    musicas = Musica.query.all()
    alfabeto = parseAlfabeto(musicas)
    return render_template('letras/letras.html', alfabeto=alfabeto)

