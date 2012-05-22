import os

import cherrypy
from google.appengine.api import users

import pystache

renderer = pystache.Renderer(search_dirs = [
        os.path.join(os.path.dirname(__file__), '../views')])

class Base:
    def render(self, name, *context, **kwargs):
        content = renderer.render(
            renderer.load_template(name), *context, **kwargs)

        # We're about to display the flash message, so we should get rid of the
        # cookie containing it.
        cherrypy.response.cookie['flash'] = ''
        cherrypy.response.cookie['flash']['expires'] = 0
        cherrypy.response.cookie['flash']['path'] = '/'
        flash = cherrypy.request.cookie.get('flash')

        return renderer.render(
            renderer.load_template("layout"),
            content = content,
            logged_in = users.get_current_user() is not None,
            login_url = users.create_login_url(cherrypy.url()),
            logout_url = users.create_logout_url(cherrypy.url()),
            message = flash and flash.value)

    def flash(self, message):
        cherrypy.response.cookie['flash'] = message
        cherrypy.response.cookie['flash']['path'] = '/'