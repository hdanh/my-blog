from wtforms import Form, TextField, PasswordField,BooleanField, validators

class LoginForm(Form):
    username = TextField(u'Username', validators=[validators.required()])
    password = PasswordField(u'Password', validators=[validators.required()])
    remember_me = BooleanField(u'Remember Me')