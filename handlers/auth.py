from base import BaseHandler
from forms.auth.auth_forms import LoginForm, SignupForm

class LoginHandler(BaseHandler):
  """Login handler"""
  def get(self):
    self._serve_page()

  def post(self):
    form = LoginForm(formdata=self.request.params)
    try:
      u = self.auth.get_user_by_password(form.username,
        form.password, remember=True, save_session=True)
      self.redirect(self.uri_for('home'))
    except (InvalidAuthIdError, InvalidPasswordError) as e:
      logging.info('Login failed for user %s because of %s', username, type(e))
      self._serve_page(True)

  def _serve_page(self, failed=False):
    form = LoginForm(formdata=self.request.params)
    params = {
        'form': form,
        'failed': failed
    }
    self.render_template('views/auth/signin.html', params)

class SignupHandler(BaseHandler):
  def get(self):
    self.render_template('views/user/signup.html')

  def post(self):
    user_name = self.request.get('username')
    email = self.request.get('email')
    name = self.request.get('name')
    password = self.request.get('password')
    last_name = self.request.get('lastname')

    unique_properties = ['email_address']
    user_data = self.user_model.create_user(user_name,
      unique_properties,
      email_address=email, name=name, password_raw=password,
      last_name=last_name, verified=False)
    if not user_data[0]: #user_data is a tuple
      self.display_message('Unable to create user for email %s because of \
        duplicate keys %s' % (user_name, user_data[1]))
      return

    user = user_data[1]
    user_id = user.get_id()

    token = self.user_model.create_signup_token(user_id)

    verification_url = self.uri_for('verification', type='v', user_id=user_id,
      signup_token=token, _full=True)

    msg = 'Send an email to user in order to verify their address. \
          They will be able to do so by visiting  <a href="{url}">{url}</a>'

    self.display_message(msg.format(url=verification_url))
