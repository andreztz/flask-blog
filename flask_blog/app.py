import os
from flask import Flask

from flask_blog.ext import bootstrap
from flask_blog.ext import cli
from flask_blog.ext import db

from flask_blog.filters import date

from flask_blog.blueprints import admin
from flask_blog.blueprints import blog


class Config:
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")
    # ?check_same_thread=False ????????
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{APPLICATION_DIR}/blog.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_ENABLE_MARKDOWN = True
    FLASK_ADMIN_SWATCH = "simplex"
    POST_PER_PAGE = 10
    ARTICLE_EDITOR = "simplemde"  # "ckeditor"


def initialize_extensions(app):
    db.configure(app)
    cli.configure(app)
    bootstrap.configure(app)


def initialize_filters(app):
    date.config(app)


def register_blueprints(app):
    admin.configure(app)
    blog.configure(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    initialize_extensions(app)
    initialize_filters(app)
    register_blueprints(app)
    return app
