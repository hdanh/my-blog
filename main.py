'''
Created on Sep 5, 2014

@author: Chip
'''
from google.appengine.ext import ndb

import logging
import webapp2

from webapp2_extras import auth
from webapp2_extras import sessions

from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
import os

import webapp2
import jinja2
#5655edb0-e107-42ba-8109-9b7837e078be - just a secret key

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

config = {
  'webapp2_extras.auth': {
    'user_model': 'models.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': '5655edb0-e107-42ba-8109-9b7837e078be'
  }
}

class BaseHandler(webapp2.RequestHandler):
  @webapp2.cached_property
  def auth(self):
    """Shortcut to access the auth instance as a property."""
    return auth.get_auth()
 
  @webapp2.cached_property
  def user_info(self):
    """Shortcut to access a subset of the user attributes that are stored
    in the session.
 
    The list of attributes to store in the session is specified in
      config['webapp2_extras.auth']['user_attributes'].
    :returns
      A dictionary with most user information
    """
    return self.auth.get_user_by_session()
 
  @webapp2.cached_property
  def user(self):
    """Shortcut to access the current logged in user.
 
    Unlike user_info, it fetches information from the persistence layer and
    returns an instance of the underlying model.
 
    :returns
      The instance of the user model associated to the logged in user.
    """
    u = self.user_info
    return self.user_model.get_by_id(u['user_id']) if u else None
 
  @webapp2.cached_property
  def user_model(self):
    """Returns the implementation of the user model.
 
    It is consistent with config['webapp2_extras.auth']['user_model'], if set.
    """   
    return self.auth.store.user_model
 
  @webapp2.cached_property
  def session(self):
      """Shortcut to access the current session."""
      return self.session_store.get_session(backend="datastore")
 
  def render_template(self, template_name, template_values={}):

    template = JINJA_ENV.get_template(template_name)
    user = self.user_info
    template_values['user'] = user
    self.response.write(template.render(template_values))

 
  def display_message(self, message):
    """Utility function to display a template with a simple message."""
    params = {
      'message': message
    }
    self.render_template('message.html', params)
 
  # this is needed for webapp2 sessions to work
  def dispatch(self):
      # Get a session store for this request.
      self.session_store = sessions.get_store(request=self.request)
 
      try:
          # Dispatch the request.
          webapp2.RequestHandler.dispatch(self)
      finally:
          # Save all sessions.
          self.session_store.save_sessions(self.response)

class SignupHandler(BaseHandler):
  def get(self):
    self.render_template('signup.html')
 
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

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('index.html')
        template_values = {}
        self.response.write(template.render(template_values))

class Contact(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENV.get_template('contact.html')
		template_values = {}
		self.response.write(template.render(template_values))
        
        

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/contact', Contact)
])