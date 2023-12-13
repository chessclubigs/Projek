from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from website.routes.views import views
from website.routes.auth import auth
from website.settings import Settings

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_class=Settings):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Settings)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app