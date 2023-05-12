from flask import Blueprint, render_template

pages_blueprint = Blueprint('pages', __name__)


@pages_blueprint.route("/")
def index():
  return render_template("index.html.j2", page_title="Hello World")


@pages_blueprint.route("/about")
def about():
  return render_template("about.html.j2")
