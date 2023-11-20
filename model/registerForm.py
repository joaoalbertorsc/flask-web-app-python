from wtforms import Form, StringField,validators,PasswordField
class RegisterForm(Form):
    name = StringField('Name', [validators.length(min = 1, max = 50)])
    username = StringField('Username', [validators.length(min = 4, max = 30)])
    email = StringField('E-mail', [validators.length(min = 6, max = 50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords do not match')
        ]
    )
    confirm = PasswordField('Confirm password')

# Queries