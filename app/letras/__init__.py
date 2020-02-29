from flask import Blueprint

bp_letras = Blueprint('bp_letras', __name__)


from . import apagar, editar, enviar, revisar, visualizar