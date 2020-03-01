from flask import Blueprint

bp_usuarios = Blueprint('bp_usuarios', __name__)


from . import auth, pass_reset, perfil, novo_revisor