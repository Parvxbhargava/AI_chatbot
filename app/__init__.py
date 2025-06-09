from flask import Flask
from dotenv import load_dotenv
from app.config import Config
from app.extensions import db,login_manager
from app.models import User 
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt()

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

def create_app():
  load_dotenv()
  app=Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  login_manager.login_view="auth.login"

  from .routes import main
  from .auth import auth

  app.register_blueprint(main)
  app.register_blueprint(auth)

  return app



