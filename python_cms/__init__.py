from flask import Flask
from os import environ
from flask_login import LoginManager
from python_cms.blueprints.pages import pages_blueprint
from python_cms.blueprints.auth import auth_blueprint
from python_cms.db import db

from python_cms.models.user import UserModel
from python_cms.models.post import PostModel

app = Flask(__name__)

app.register_blueprint(pages_blueprint)
app.register_blueprint(auth_blueprint)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

app.secret_key = environ.get("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
  return UserModel.get(user_id)


# @app.before_first_request
# def create_tables():
#   db.create_all()

# USE THIS INSTEAD
with app.app_context():
  print("Creating tables...")
  db.create_all()
