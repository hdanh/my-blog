from wtforms import Form, TextField, PasswordField,BooleanField, validators

class LoginForm(Form):
  username = TextField(u'Username', validators=[validators.Required()])
  password = PasswordField(u'Password', validators=[validators.Required()])
  remember_me = BooleanField(u'Remember Me')

class SignupForm(Form):
  first_name = TextField(u'First Name', validators=[validators.Required()])
  last_name = TextField(u'Last Name', validators=[validators.Required()])
  email = TextField(u'Email', validators=[validators.Required(), validators.Email()])
  pwd = PasswordField('Password',
    validators=[
      validators.Required(),
      validators.EqualTo('confirm_pwd'),
      validators.Length(min=6, max=20)])
  confirm_pwd = PasswordField('Confirm password')

class ChangePassForm(Form):
  current_pwd = PasswordField('Current Password', validators=[validators.Required()])
  new_pwd = PasswordField('New Password',
    validators=[
      validators.Required(),
      validators.EqualTo('confirm_pwd'),
      validators.Length(min=6, max=20)])
  confirm_pwd = PasswordField('Confirm password')
