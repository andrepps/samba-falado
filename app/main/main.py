from flask import render_template
from app.models import Musica, Compositor
from . import bp_main


@bp_main.route('/')
def main():
    nl = len(Musica.query.all())
    nc = len(Compositor.query.all())
    return render_template('main.html', nc=nc, nl=nl)