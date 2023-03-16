from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_assets import Bundle, Environment

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
    login_manager.init_app(app)

    from models import User,AdminUser,Employer
    @login_manager.user_loader
    def load_user(user_id):
        user_type = User.query.get(int(user_id))
        if user_type is None:
            return AdminUser.query.get(int(user_id))
        if user_type is None:
            return Employer.query.get(int(user_id))
        return user_type

    from adminpanel import adminpanel as adminpanel_blueprint
    app.register_blueprint(adminpanel_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from candidate import candidate as candidate_blueprint
    app.register_blueprint(candidate_blueprint)

    from employer import employer as employer_blueprint
    app.register_blueprint(employer_blueprint)

    login_manager.blueprint_login_views = {
    'adminpanel': 'auth.admin_login',
    'candidate': 'auth.user_login',
    'employer': 'auth.emp_login',
    }

    assets = Environment(app)
    css = Bundle("src/main.css", output="dist/main.css")
    js = Bundle("src/*.js", output="dist/main.js") # new

    assets.register("css", css)
    assets.register("js", js) # new
    css.build()
    js.build() # new


    return app

