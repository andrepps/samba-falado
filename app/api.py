from flask import Blueprint, jsonify
from app.serializer import CompositorSchema, MusicaSchema
from app.models import Compositor, Musica

api = Blueprint('api', __name__)

@api.route('/api/musicas/')
def getJsonMusicas():
    musicas = Musica.query.all()[::-1]
    json_data = MusicaSchema(many=True).jsonify(musicas)
    return json_data # dump, dumps, jsonify


@api.route('/api/compositores')
def getJsonCompositores():
    compositores = Compositor.query.all()[::-1]
    json_data = CompositorSchema(many=True).jsonify(compositores)
    return json_data