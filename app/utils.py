from PIL import Image
from flask_mail import Message
import secrets
import os
from app import mail
from unidecode import unidecode
from flask import current_app, url_for


def avisar_novo_revisor(usuario):
    msg = Message('Convite para se tornar revisor do site Samba Falado', 
                    sender=('Samba Falado', 'sambafalado@gmail.com'),
                    recipients=[usuario.email]
                    )
    msg.body = 'VocÊ agora é revisor do Samba Falado!'
    mail.send(msg)


#def revisor_token(usuario):
#    token = usuario.get_token(172800)
#    msg = Message('Convite para se tornar revisor do site Samba Falado', 
#                    sender=('Samba Falado', 'sambafalado@gmail.com'),
#                    recipients=[usuario.email])
#    msg.body = f'''Você recebeu um convite para se tornar revisor das letras enviadas para o Samba Falado. Para aceitar acesse o link
#    {url_for('bp_usuarios.novo_revisor', token=token, _external=True)}
#    '''
#    mail.send(msg)##


def enviar_token(usuario):
    token = usuario.get_token()
    msg = Message('Recuperar Senha', 
                    sender=('Samba Falado', 'sambafalado@gmail.com'),
                    recipients=[usuario.email])
    msg.body = f'''Para recuperar sua senha, acesse o link:
    {url_for('bp_ususarios.nova_senha', token=token, _external=True)}
                    
    Se você não requisitou a recuperação de senha ignore esta mensagem!
    '''
    mail.send(msg)


def save_pic(form_pic):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_pic.filename)
    foto_filename = random_hex + f_ext
    foto_path = os.path.join(current_app.root_path, 'static/images/profile_pics', foto_filename)
    
    output_size = (150,150)
    i = Image.open(form_pic)
    tamanho = min(i.size)
    xcenter = i.width/2
    ycenter = i.height/2
    x1 = xcenter - tamanho/2
    x2 = xcenter + tamanho/2
    y1 = ycenter - tamanho/2
    y2 = ycenter + tamanho/2
    i = i.crop((x1,y1,x2,y2))
    i.thumbnail(output_size)

    i.save(foto_path)
    return foto_filename


def parseAlfabeto(data):
    alfabeto = {}
    data = sorted(data, key=lambda x: x.nome, reverse=False)
    for item in data:
        primeira_letra = unidecode(item.nome[0])
        if primeira_letra not in alfabeto.keys():
            alfabeto[primeira_letra] = [item]
        else:
            alfabeto[primeira_letra].append(item) 
    return alfabeto


def parseComp(compositores):
    comp = []
    for compositor in compositores:
        comp.append(compositor.nome)
    s = ', '
    return s.join(comp)