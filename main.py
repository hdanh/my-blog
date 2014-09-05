'''
Created on Sep 5, 2014

@author: Chip
'''
import os

import webapp2
import jinja2

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENV.get_template('index.html')
        template_values = {}
        self.response.write(template.render(template_values))
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
])