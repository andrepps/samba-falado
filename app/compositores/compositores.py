from . import bp_compositores

from flask import render_template
from app.models import Compositor
from app.utils import parseAlfabeto

@bp_compositores.route('/compositores/<int:id>/')
def compositor(id):
    compositor = Compositor.query.get_or_404(id)
    return render_template('compositores/compositor.html', compositor=compositor)

@bp_compositores.route('/compositores/')
def compositores():
    compositores = Compositor.query.all()
    alfabeto = parseAlfabeto(compositores)
    return render_template('compositores/compositores.html', alfabeto=alfabeto)    