from flask import render_template
from flask import Blueprint
from flask import request
from sqlalchemy import text
from ..models import Post, Tag

bp = Blueprint("blog", __name__)


@bp.route("/blog/", methods=["GET"])
@bp.route("/blog/<int:page>", methods=["GET"])
def index(page=1):
    per_page = 5
    # paginator error flag.
    # If True, when an out of range page is requested a 404 error will be
    # automatically returned to the client. If False, an empty list will be
    # returned for out of range pages.
    # entries = Post.query.paginate(1, 20, False).items
    # entries = Post.query.order_by("created_timestamp desc").paginate(
    #     page, per_page, False
    # )
    entries = Post.query.order_by(text("created_timestamp desc")).paginate(
        page, per_page, False
    )
    return render_template("blog/index.html", entries=entries)


@bp.route("/post")
@bp.route("/post/<int:_id>", methods=["GET"])
def post(_id):
    post = Post.query.filter(Post.id == _id).first()
    return render_template("blog/post.html", post=post)


@bp.route("/")
def about():
    return render_template("blog/about.html")


def configure(app):
    app.register_blueprint(bp)
