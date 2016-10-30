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
            html = '<h1>I\'m a document!</h1>'
        else:
            html = document.file.read()

        docraptor.configuration.username = "ONweg0Cg51Sb6erdp9"
        # this key works for test documents

        doc_api = docraptor.DocApi()

        # response = doc_api.create_doc({
        #     "test": True,
        #     "document_content": html,
        #     "name": "docraptor-python.pdf",
        #     "document_type": "pdf",
        # })

        # file = open("/tmp/docraptor-python.pdf", "wb")
        # file.write(response)
        # file.close
        # logging.critical("Wrote PDF to /tmp/docraptor-python.pdf")

        # self.response.write(response)

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
                    # file = open("/tmp/docraptor-python.pdf", "wb")
                    # file.write(doc_response)
                    # file.close
                    # logging.critical("Wrote PDF to /tmp/docraptor-python.pdf")
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
                    time.sleep(0.5)

        except docraptor.rest.ApiException as error:
            logging.critical(error)
            logging.critical(error.message)
            logging.critical(error.code)
            logging.critical(error.response_body)



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/api/doc', RenderPdf),
], debug=True)
