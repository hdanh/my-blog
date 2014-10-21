from base import BaseHandler

class IndexHandler(BaseHandler):
  def get(self):
    self.render_template('views/blogs/index.html')
