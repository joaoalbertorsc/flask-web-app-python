from wtforms import Form, StringField,TextAreaField,validators

class ArticleForm(Form):
    title = StringField('Title', [validators.length(min = 1, max = 200)])
    body = TextAreaField('Body', [validators.length(min = 30)])