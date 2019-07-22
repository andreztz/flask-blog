from wtforms import fields, widgets


class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("class_", "ckeditor")
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(fields.TextField):
    widget = CKTextAreaWidget()


class SimpleMDEAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault("class_", "simplemde")
        return super(SimpleMDEAreaWidget, self).__call__(field, **kwargs)


class SimpleMDEAreaField(fields.TextField):
    widget = SimpleMDEAreaWidget()


ARTICLE_EDITOR = "simplemde"

if ARTICLE_EDITOR == "ckeditor":
    EDITOR_WIDGET = CKTextAreaField
else:
    EDITOR_WIDGET = SimpleMDEAreaField
