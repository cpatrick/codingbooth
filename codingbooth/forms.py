from flask.ext.wtf import Form, TextField, PasswordField, validators


class LoginForm(Form):
    email = TextField('Email', [validators.Length(min=4, max=25)])
    password = PasswordField('Password')


class RegistrationForm(Form):
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
