import cgi
import os
import re
import urllib
import logging
import time
import shutil
import datetime
import json

import webapp2
import jinja2
import docraptor

from doc_generator import generate_pdf

from google.appengine.api import urlfetch

from secretvalue import SecretValue


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/main.html')
        self.response.write(template.render())


class RenderPdf(webapp2.RequestHandler):

    def post(self):

        def callback_function(duration=0, error=None, **kwargs):
            if error:
                logging.critical(error)
                return
            if 'doc_response' in kwargs:
                doc_response = kwargs['doc_response']
            logging.info("PDF generated in ~{}ms".format(duration))
            self.response.out.write(doc_response)
            self.response.headers.add_header(
                "Content-disposition", "attachment")
            self.response.headers.add_header(
                "Content-type", "application/pdf")

        # Arguments to be used by the PDF generation function
        kwargs = {}

        document = self.request.POST.getall('attachments')[0]
        if isinstance(document, unicode):
            template_data = {}
            now = datetime.datetime.now()
            template_data['monthyear'] = now.strftime("%B %Y")
            template_name = 'templates/reports/example.html'
            html = render_template(template_name, **template_data)
            logging.info("Generating PDF from: {}".format(template_name))
        else:
            html = document.file.read()
            # Check if style embedder is checked
            if self.request.get('generate_toc') == 'on':
               kwargs['build_toc'] = True
            # Check if style embedder is checked
            if self.request.get('embed_styles') == 'on':
                kwargs['include_default_styles'] = True

        # Init DocRaptor Api
        docraptor_username = SecretValue.get_by_id('docraptor_username')
        if docraptor_username is None:
            logging.error('No "docraptor_username" value set with SecretValue')
            self.response.out.write('Please set "docraptor_username" with SecretValue')
            return

        # Determine if we'll be using test mode or not.
        access_code = SecretValue.get_by_id('access_code')
        if access_code is not None:
            if (access_code.value == self.request.get('access_code')):
                kwargs['is_production'] = True
        else:
            logging.error('No "access_code" value set with SecretValue')

        generate_pdf(docraptor_username.value, html, callback_function,
            **kwargs)


class SecretValues(webapp2.RequestHandler):
    """For securely storing secret values."""

    def get(self, id):
        # if not app_engine_users.is_current_user_admin():
        #     raise PermissionDenied()
        logging.info('Fetching secret value')
        exists = SecretValue.get_by_id(id) is not None
        self.response.out.write(json.dumps(
            {'key exists': exists,
             'message': "SecretValues can't be read via api urls."}))

    def post(self, id):
        # if not app_engine_users.is_current_user_admin():
        #     raise PermissionDenied()
        value = self.request.params.get('value', None)
        if value is None:
            raise Exception("Must POST with a value.")
        sv = SecretValue.get_or_insert(id)
        sv.value = value
        sv.put()
        self.response.out.write(id)

    def delete(self, id):
        # if not app_engine_users.is_current_user_admin():
        #     raise PermissionDenied()
        sv = SecretValue.get_by_id(id)
        if sv is not None:
            sv.key.delete()
        self.response.out.write(id)


class ViewHtml(webapp2.RequestHandler):
    def get(self, filename):
        template = JINJA_ENVIRONMENT.get_template(
            'templates/{}.html'.format(filename))
        self.response.write(template.render())


# Loads html from a template using jinja2
def render_template(template, **template_data):
    return JINJA_ENVIRONMENT.get_template(template).render(**template_data)


application = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='home'),
    webapp2.Route(r'/view/<filename>', handler=ViewHtml, name='view_html'),
    webapp2.Route(r'/api/doc', handler=RenderPdf, name='render_pdf'),
    webapp2.Route(r'/api/secret_values/<id>', handler=SecretValues, name='secret_values'),
], debug=True)
