from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os 
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

def create_app():
    app = Flask(__name__) 
    app.config['SECRET_KEY'] = os.getenv("SQLALCHEMY_SECRET_KEY")
    basedir = os.getcwd()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{basedir}/{os.getenv("SQLALCHEMY_DATABASE_URI")}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' 

    login_manager.init_app(app)

    from models import User,adminUser
    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))
    '''
    @login_manager.user_loader
    def load_admin_user(admin_id):

        return adminUser.query.get(int(admin_id))
    '''
    from adminpanel import adminpanel as adminpanel_blueprint
    app.register_blueprint(adminpanel_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)



    return app

