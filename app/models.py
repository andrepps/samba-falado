from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(usuario_id):
    return Usuario.query.get(int(usuario_id))

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    senha = db.Column(db.String, nullable=False)
    permissao = db.Column(db.Integer, 
        nullable=False, default=0)
    foto = db.Column(db.String, 
        nullable=False, default='default.png')
    letras_enviadas = db.relationship('Musica', 
                                    backref='enviado_por',
                                    lazy='dynamic'
                                    )
    letras_em_revisao = db.relationship('EmRevisao', 
                                    backref='enviado_por',
                                    lazy='dynamic'
                                    )
    cadastrado_em = db.Column(db.DateTime, 
                            nullable=False, 
                            default=datetime.utcnow)

    def get_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Usuario.query.get(user_id) 


    def __repr__(self):
        return f"Usuario('{self.nome}', '{self.email}', '{self.permissao}')"



compositores = db.Table('compositores', 
                    db.Column('compositor_id', 
                    db.Integer, 
                    db.ForeignKey('compositor.id')),
                    db.Column('musica_id', 
                    db.Integer, 
                    db.ForeignKey('musica.id'))
                    )

class Musica(db.Model):
    __tablename__ = 'musica'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    letra = db.Column(db.Text, nullable=False)
    compositores = db.relationship('Compositor', 
                                    secondary=compositores, 
                                    backref=db.backref('musicas', lazy='dynamic'),
                                    lazy='dynamic'
                                    )
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)                                
    enviado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    informacoes = db.Column(db.Text)

    def __repr__(self):
        return f"Musica('musica: {self.nome}', enviada por:'{self.enviado_por}')"           


class Compositor(db.Model):
    __tablename__ = 'compositor'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    informacoes = db.Column(db.Text)
    foto = db.Column(db.String, nullable=False, default='default.png')


    def __repr__(self):
        return f"Compositor('{self.nome}')"
                         
 

class EmRevisao(db.Model):
    __tablename__ = 'emrevisao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable = False)
    compositores = db.Column(db.String, nullable=False)
    letra = db.Column(db.Text, nullable=False)
    informacoes = db.Column(db.Text)
    enviado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)                                

    