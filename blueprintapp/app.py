from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.secret_key = 'SOME KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./testdb.db'


    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('login'))
    
    bcrypt = Bcrypt(app)

    from routes import register_routes
    register_routes(app, db, bcrypt)

    migrate = Migrate(app, db)
    return app