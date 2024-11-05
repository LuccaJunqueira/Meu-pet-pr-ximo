from flask import Flask
from .config import Config
from .db import get_db_connection

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.jinja_env.globals.update(get_db_connection=get_db_connection)

    from .routes.api import api_bp
    from .routes.main import main_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(main_bp)

    return app
