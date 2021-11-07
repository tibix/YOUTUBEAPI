from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def create_app(*args, **kwargs):
    env = kwargs['env']
    app = Flask(__name__)
    app.config.from_object('conf.%s' % env)
    db.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app

