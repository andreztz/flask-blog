import re
from flask import redirect
from flask import request
from flask import url_for

from flask_admin import Admin
from flask_admin import AdminIndexView
from flask_admin import expose
from flask_admin import helpers
from flask_admin.contrib.sqla import ModelView


from flask_login import current_user
from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from wtforms import fields
from wtforms import form
from wtforms import validators

from flask_blog.ext.db import db
from ..models import Post, Tag, User


from .widgets import EDITOR_WIDGET


def slugify(string):
    return re.sub("[^\w]+", "-", string).lower()


class LoginForm(form.Form):

    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError("Invalid user")

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError("Invalid password")

    def get_user(self):
        return db.session.query(User).filter_by(login=self.login.data).first()


class RegistrationForm(form.Form):

    login = fields.StringField(validators=[validators.required()])
    email = fields.StringField()
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        if db.session.query(User).filter_by(login=self.login.data).count() > 0:
            raise validators.ValidationError("Duplicate username")


class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super().index()

    @expose("/login", methods=["GET", "POST"])
    def login_view(self):
        form = LoginForm(request.form)

        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

        if current_user.is_authenticated:
            return redirect(url_for(".index"))

        link = (
            "<p>Don't have an account? <a href=\""
            + url_for(".register_view")
            + '">Click here to register.</a></p>'
        )
        self._template_args["form"] = form
        self._template_args["link"] = link
        return super().index()

    @expose("/register/", methods=["GET", "POST"])
    def register_view(self):
        form = RegistrationForm(request.form)

        if helpers.validate_form_on_submit(form):
            user = User()
            form.populate_obj(user)
            user.password = generate_password_hash(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for(".index"))

        link = (
            '<p>Already have an account? <a href="'
            + url_for(".login_view")
            + '">Click here to log in.</a></p>'
        )
        self._template_args["form"] = form
        self._template_args["link"] = link
        return super().index()

    @expose("/logout/")
    def logout_view(self):
        logout_user()
        return redirect(url_for(".index"))


class PostView(ModelView):
    def _text_formatter(view, context, model, name):
        return model.body[:30] + " ..."

    def _slug_formatter(view, context, model, name):
        return model.slug[:20] + "..."

    page_size = 10

    # column_searchable_list = ( Post.title, Tag.name )
    column_searchable_list = ("title", "status")
    column_list = [
        "title",
        "body",
        "slug",
        "created_timestamp",
        "modified_timestamp",
        "status",
    ]
    column_labels = {  # modifica nomes das colunas
        "created_timestamp": "created",
        "modified_timestamp": "modified",
    }
    column_default_sort = (
        "created_timestamp",
        True,
    )  # exibe o conteído por ordem de criação
    column_formatters = {"body": _text_formatter, "slug": _slug_formatter}
    # form_overrides = dict(body=CKEditorField)
    # form_overrides = dict(body=PageDownField)
    form_overrides = dict(body=EDITOR_WIDGET)
    can_view_details = True
    create_template = "admin/create.html"
    edit_template = "admin/edit.html"

    def on_model_change(self, form, model, is_created):
        model.slug = slugify(model.title)

    def is_accessible(self):
        return current_user.is_authenticated


class TagView(ModelView):

    form_columns = ("name", "slug")
    form_create_rules = ("name", "slug")

    def on_model_change(self, form, model, is_created):
        model.slug = slugify(model.name)

    def is_accessible(self):
        return current_user.is_authenticated


def configure(app):
    app.admin = Admin(
        app,
        name="DashBoard",
        template_mode="bootstrap3",
        index_view=MyAdminIndexView(),
        base_template="admin/my_master.html",
    )
    app.admin.add_view(PostView(Post, db.session, "Posts"))
    app.admin.add_view(TagView(Tag, db.session, "Tags"))

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)
