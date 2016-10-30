import docraptor

docraptor.configuration.username = "ONweg0Cg51Sb6erdp9"
# this key works for test documents

doc_api = docraptor.DocApi()

response = doc_api.create_doc({
    "test": True,                                                   # test documents are free but watermarked
    "document_content": "<html><body>Hello World</body></html>",    # supply content directly
    # "document_url": "http://docraptor.com/examples/invoice.html", # or use a url
    "name": "docraptor-python.pdf",                                 # help you find a document later
    "document_type": "pdf",                                         # pdf or xls or xlsx
    # "javascript": True,                                           # enable JavaScript processing
    # "prince_options": {
    #   "media": "screen",                                          # use screen styles instead of print styles
    #   "baseurl": "http://hello.com",                              # pretend URL when using document_content
    # },
})
