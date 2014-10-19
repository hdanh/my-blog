'''
Created on Sep 5, 2014

@author: Chip
'''

import os
import sys
import webapp2
import jinja2

#5655edb0-e107-42ba-8109-9b7837e078be - just a secret key

root_dir = os.path.dirname(__file__)
sys.path.insert(0, 'libs')

config = {
  'webapp2_extras.auth': {
    'user_model': 'models.user.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': '5655edb0-e107-42ba-8109-9b7837e078be'
  }
}

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler='handlers.home.MainHandler', name='home'),
    webapp2.Route('/contact', handler='handlers.contact.ContactHandler', name='contact'),
    webapp2.Route('/signup', handler='handlers.signup.SignupHandler', name='signup'),
    webapp2.Route('/login', handler='handlers.login.LoginHandler', name='login'),
    webapp2.Route('/blogs', handler='handlers.blogs.IndexHandler', name='blogs')
], config=config)
