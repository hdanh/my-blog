from base import BaseHandler
from forms import login_form

class LoginHandler(BaseHandler):
    """Login handler"""
    def get(self):
        self._serve_page()

    def post(self):
        form=login_form.LoginForm(formdata=self.request.params)

    def _serve_page(self, failed=False):
        form=login_form.LoginForm(formdata=self.request.params)
        params= {
            'form': form,
            'failed': failed
        }
        self.render_template('views/login.html', params)
