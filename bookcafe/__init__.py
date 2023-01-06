from flask import Flask
from .extentions import db, migrate,ma
from . import db, ma
from .api.api import api
from .api.view import view
from .api.auth import auth
from bookcafe.model.users import User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='BookCafetesyafdag'
    app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    app.register_blueprint(api, url_prefix='/api/v1')
    app.register_blueprint(view)
    app.register_blueprint(auth, url_prefix='/auth/v1')

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(str(id))




    return app


