import datetime

from flask_blog.ext.db import db


import mistune

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


# pygmentize -S default -f html -a .highlight > default.css
class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return "\n<pre><code>%s</code></pre>\n" % mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


def markdown(content):
    return mistune.Markdown(renderer=HighlightRenderer())(content)


def slugify(string):
    return re.sub("[^\w]+", "-", string).lower()


entry_tags = db.Table(
    "entry_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)


class Post(db.Model):

    STATUS_PUBLIC = 0
    STATUS_DRAFT = 1

    id = db.Column(db.Integer, primary_key=True)
    # falha ao add novo post com mesmo titulo  UNIQUE constraint failed: entry.slug
    title = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    body = db.Column(db.Text)
    status = db.Column(db.SmallInteger, default=STATUS_PUBLIC)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    tags = db.relationship(
        "Tag", secondary=entry_tags, backref=db.backref("post", lazy="dynamic")
    )

    @property
    def to_html(self):
        return markdown(self.body)

    def __repr__(self):
        return "<Entry: {}>".format(self.title)

    def __str__(self):
        return "{}".format(self.title)


class Tag(db.Model):
    """Para buscar entradas atraves das tags use
       qualquertag.entries.all()
       isso foi definido na tabela Post no atributo tags
       o atributo tags tem a ref. entries.  [º_°]
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    slug = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Tag {}>".format(self.name)

    def __str__(self):
        return "{}".format(self.name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username
