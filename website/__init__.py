from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS

from website.settings import Settings

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
cors = CORS()

def create_app(config_class=Settings):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Settings)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    migrate.init_app(app, db)
    cors.init_app(app)

    from website.routes.views import views
    from website.routes.auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @login_manager.user_loader
    def load_user(user_id):
        from website.models import User
        return User.query.get(int(user_id))

    return app