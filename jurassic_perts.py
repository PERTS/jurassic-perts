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
        document = self.request.POST.getall('attachments')[0]
        template_data = {}
        now = datetime.datetime.now()
        template_data['monthyear'] = now.strftime("%B %Y")
        if isinstance(document, unicode):
            template_name = 'templates/reports/example.html'
            html = render_template(template_name, **template_data)
            logging.info("Generating PDF from: {}".format(template_name))
        else:
            html = document.file.read()
            # Check if style embedder is checked
            if self.request.get('embed_styles') == 'on':
                logging.info('Embedding default styles for PDF')
                # @todo: embed CSS from 'templates/reports/_styles.html'
                # -- before the </head> element in the document
                # -- or create <head></head> and inject in there
                if '</head>' in html:
                    logging.info('Head found.')
                else:
                    logging.info('No head found, creating...')
                    # Find <body> and inject before that
                    body_loc = html.index('<body>')
                    html = "{}<head></head>{}".format(
                        html[:body_loc], html[body_loc:])

                # Fetch styles html
                styles_template = 'templates/reports/_styles.html'
                styles_html = render_template(styles_template)

                # Find </head> and inject styles before that
                head_loc = html.index("</head>")
                html = "{}{}{}".format(
                    html[:head_loc], styles_html, html[head_loc:])

        # Init DocRaptor Api
        docraptor_username = SecretValue.get_by_id('docraptor_username')
        if docraptor_username is None:
            logging.error('No "docraptor_username" value set with SecretValue')
            self.response.out.write('Please set "docraptor_username" with SecretValue')
            return
        docraptor.configuration.username = docraptor_username.value
        doc_api = docraptor.DocApi()

        # Determine if we'll be using test mode or not.
        test_mode = True;
        access_code = SecretValue.get_by_id('access_code')
        if access_code is not None:
            test_mode = (access_code.value != self.request.get('access_code'))
        else:
            logging.error('No "access_code" value set with SecretValue')

        # Variables for tracking generation time
        time_counter = 0
        sleep_increment = 0.1  # in seconds

        try:
            create_response = doc_api.create_async_doc({
                "test": test_mode,         # test documents are free but watermarked
                "document_content": html,           # supply content directly
                "name": "docraptor-python.pdf",     # help find document later
                "document_type": "pdf",             # pdf or xls or xlsx
                "prince_options": {
                    "javascript": True             # generated content in js
                    # 'baseurl': 'https://s3.amazonaws.com'
                }
            })

            while True:
                status_response = doc_api.get_async_doc_status(create_response.status_id)
                if status_response.status == "completed":
                    doc_response = doc_api.get_async_doc(status_response.download_id)
                    logging.info("PDF generated in ~{}ms".format(
                        time_counter * sleep_increment * 1000))
                    self.response.out.write(doc_response)
                    self.response.headers.add_header(
                        "Content-disposition", "attachment")
                    self.response.headers.add_header(
                        "Content-type", "application/pdf")
                    break
                elif status_response.status == "failed":
                    logging.critical("FAILED")
                    logging.critical(status_response)
                    break
                else:
                    time_counter += 1
                    time.sleep(sleep_increment)

        except docraptor.rest.ApiException as error:
            logging.critical(error)
            logging.critical(error.message)
            logging.critical(error.code)
            logging.critical(error.response_body)


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
