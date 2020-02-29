from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

from app import db
from app.models import Musica, Compositor, Usuario
from flask_bcrypt import Bcrypt


bs = BeautifulSoup
novo_user = Usuario(nome='Samba Falado', 
                    email='sambafalado@email.com', 
                    senha=Bcrypt().generate_password_hash('heitor').decode('utf-8'), 
                    permissao='2')
db.session.add(novo_user)
for ano in range(2009,2014):
    for mes in range(1,13):
        url = 'http://sambafalado.blogspot.com/'+str(ano)+'/'+str(mes).zfill(2)+'/'
        print(url)
        source = requests.get(url).text
        
        soup = bs(source,'lxml')
        for result in soup.find_all('div', class_='post-outer'):
            
            result_datetime = result.abbr['title']
            print('result_datetime')
            result_datetime = datetime.fromisoformat(result_datetime)

            result_letra = result.find('div', class_='post-body entry-content')
            for br in result_letra.find_all('br'):
                br.replace_with('\n')
            letra_da_musica = result_letra.text

            result_titulo = result.find('h3', class_='post-title entry-title')
            result_titulo = result_titulo.a.text.split('(')
            
            nome_da_musica = result_titulo[0].strip()
            
            compositores = result_titulo[1].split(')')[0]
            compositores = re.split('&|/|-|–|,', compositores)
            striper = []
            for compositor in compositores:
                striper.append(compositor.strip())
            compositores = striper

            nova_musica = Musica(nome=nome_da_musica, 
                                letra=letra_da_musica, 
                                enviado_por=novo_user,
                                enviado_em=result_datetime)
            db.session.add(nova_musica)
            
            comps=[] ##
            for compositor in compositores:
                query_compositor = Compositor.query.filter_by(nome=compositor).first()
                if not query_compositor:
                    novo_compositor = Compositor(nome=compositor)
                    db.session.add(novo_compositor)
                    nova_musica.compositores.append(novo_compositor)
                else: nova_musica.compositores.append(query_compositor)
                comps.append(compositor) ##
            db.session.commit()
                
                
            print(f'{nome_da_musica} ({comps})') ##