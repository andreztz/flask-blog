import click

from flask_blog.ext.db import db
from flask_blog.blueprints.models import Post, Tag, User

from werkzeug.security import generate_password_hash

from .fake_data import tags, posts


def configure(app):
    """Attach new commands in to app"""

    @app.shell_context_processor
    def shell_context():
        return {"app": app, "db": db, "Post": Post, "Tag": Tag, "User": User}

    @app.cli.command()
    @click.option("--login", "-l", required=True)
    @click.option("--email", "-e", required=True)
    @click.option("--password", "-p", required=True)
    def add_user(login, email, password):
        u = User()
        u.login = login
        u.email = email
        u.password = generate_password_hash(password)
        db.session.add(u)
        db.session.commit()

    @app.cli.command()
    def init_db():
        db.create_all()
        click.echo("db criado com sucesso!")

    @app.cli.command()
    def create_fake_blog():
        db.create_all()

        u = User()
        u.login = "admin"
        u.email = "admin@gmail.com"
        u.password = generate_password_hash("admin")
        db.session.add(u)
        db.session.commit()

        fake_tags = []

        for t in tags:
            tag = Tag()
            tag.name = t
            tag.slug = t
            fake_tags.append(tag)
            db.session.add(tag)

        for p in posts:
            post = Post()
            post.title = p["title"]
            post.body = p["body"]
            post.slug = "_".join(p["title"].split(" "))
            import random

            for i in range(random.randint(1, 5)):
                post.tags.append(random.choice(fake_tags))
            db.session.add(post)

        db.session.commit()
