from app import ma
from app.models import Compositor, Musica

class initCompositorSchema(ma.ModelSchema):
    class Meta:
        model = Compositor
        fields = ('nome', '')

class MusicaSchema(ma.ModelSchema):
    compositores = ma.Nested(initCompositorSchema, many=True)
    class Meta:
        model = Musica
        fields = ('nome','letra', 'compositores')

class CompositorSchema(ma.ModelSchema):
    musicas = ma.Nested(MusicaSchema, many=True)
    class Meta:
        model = Compositor
        fields = ('nome', 'musicas')


