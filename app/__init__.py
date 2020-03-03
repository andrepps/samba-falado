from flask import Flask
from app.config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()



def create_app(config_class=Config):
    from flask import Flask
    app = Flask(__name__)
    
    app.config.from_object(config_class)
    app.jinja_env.add_extension('jinja2.ext.do')

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app,db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)    

    from .main import bp_main
    from .usuarios import bp_usuarios
    from .letras import bp_letras
    from .compositores import bp_compositores
    app.register_blueprint(bp_main, url_prefix='/sambafalado')
    app.register_blueprint(bp_usuarios, url_prefix='/sambafalado')
    app.register_blueprint(bp_letras, url_prefix='/sambafalado')
    app.register_blueprint(bp_compositores, url_prefix='/sambafalado')



    return app

