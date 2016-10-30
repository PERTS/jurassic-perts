import cgi
import os
import re
import urllib
import logging
import time
import shutil

import webapp2
import jinja2
import docraptor

from google.appengine.api import urlfetch


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
        if isinstance(document, unicode):
            template_name = 'templates/reports/example.html'
            html = render_template(template_name)
            logging.info("Generating PDF from: {}".format(template_name))
        else:
            html = document.file.read()
            # Check if style embedder is checked
            if self.request.get("embed_styles") == 'on':
                logging.info("Embedding default styles for PDF")

        docraptor.configuration.username = "ONweg0Cg51Sb6erdp9"
        # this key works for test documents

        doc_api = docraptor.DocApi()

        time_counter = 0;
        sleep_time = 0.1;

        try:
            create_response = doc_api.create_async_doc({
                "test": True,                                                   # test documents are free but watermarked
                "document_content": html,    # supply content directly
                "name": "docraptor-python.pdf",                                # help you find a document later
                "document_type": "pdf",                                         # pdf or xls or xlsx
            })

            while True:
                status_response = doc_api.get_async_doc_status(create_response.status_id)
                if status_response.status == "completed":
                    doc_response = doc_api.get_async_doc(status_response.download_id)
                    logging.info("PDF generated in ~{}ms".format(
                        time_counter * sleep_time * 1000))
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
                    time_counter += 1;
                    time.sleep(sleep_time)

        except docraptor.rest.ApiException as error:
            logging.critical(error)
            logging.critical(error.message)
            logging.critical(error.code)
            logging.critical(error.response_body)


# Loads html from a template using jinja2
def render_template(template, **template_data):
    return JINJA_ENVIRONMENT.get_template(template).render(**template_data)


application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/doc', RenderPdf),
], debug=True)
