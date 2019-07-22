from flask_ckeditor import CKEditor
from flask_pagedown import PageDown


def configure(app):
    PageDown(app)
    CKEditor(app)
