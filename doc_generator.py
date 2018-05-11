import time
import urllib
import docraptor
# Parser from https://github.com/lxml/lxml
from lxml import etree
from lxml.html import fromstring, tostring

import config

# Function builds Table of Contents based on an HTML string
# Returns HTML with adjustments for Table of Contents
def build_toc(html):
    print('Building TOC...')
    new_html = html
    # First make sure this html has a place for the html
    if 'id="toc"' not in html:
        print('No TOC ID found...')
        return html

    # Then find all header elements
    # Create a regex to find any <h1> <h2> <h3>
    # For each, 
    # - fetch the title-string and
    # - construct a parameterized string for the ID
    # - Check the number following the h and,
    # - adjust the TOC html accordingly 

    # @todo: remove this, it's just for testing
    toc = etree.Element("div", id="toc")

    # parsed_html = etree.fromstring(html)
    event_types = ("start", "end", "start-ns", "end-ns")
    parser = etree.XMLPullParser(event_types)
    events = parser.read_events()
    parser.feed(html)
    # Increases as we get deeper, helps construct TOC
    header_level = 0
    current_list = toc # append list items to main div
    last_item = toc

    for action, obj in events:
        classes = obj.get('class')
        if classes and any(x in classes for x in ['title', 'no-toc']):
            continue
        if action == 'start':
            if obj.tag == 'h1':
                if header_level > 1:
                    # Need to return to top level
                    current_list = toc
                header_level = 1
            elif obj.tag == 'h2':
                if header_level < 2:
                    # Add new level to the TOC
                    current_list = etree.SubElement(last_item, "ol")
                elif header_level > 2:
                    # Need to close current level and go up
                    current_list = current_list.getparent().getparent()
                header_level = 2
            elif obj.tag == 'h3':
                if header_level < 3:
                    # Add new level to the TOC
                    current_list = etree.SubElement(last_item, "ol")
                elif header_level > 3:
                    # Need to close current level and go up
                    current_list = current_list.getparent().getparent()
                header_level = 3
            # For any header level, we append to the header list position
            if obj.tag in ('h1', 'h2', 'h3'):
                header_text = obj.text.strip()
                # Parameterize text AND CHANGE BELOW
                param_header = header_text.lower().replace(' ', '-');
                obj.set("id", param_header)
                # Append li a with href and text to the TOC
                list_item = etree.SubElement(current_list, "li")
                anchor = etree.SubElement(
                    list_item, "a", href="#%s" % param_header)
                anchor.text = header_text
                last_item = list_item

    root = parser.close()
    new_html = tostring(root).replace('<div id="toc"></div>', tostring(toc))
    # print(new_html)
    print('TOC build complete.')
    return new_html


def insert_default_styles(html):
    print('Embedding default styles for PDF...')
    # Eembed CSS from 'templates/reports/_styles.html'
    # -- before the </head> element in the document
    # -- or create <head></head> and inject in there
    if '</head>' in html:
        print('Head found.')
    else:
        print('No head found, creating...')
        # Find <body> and inject before that
        body_loc = html.index('<body>')
        html = "{}<head></head>{}".format(
            html[:body_loc], html[body_loc:])

    # Fetch styles html
    styles_template = 'templates/reports/_styles.html'
    styles_html = urllib.urlopen(styles_template).read()

    # Find </head> and inject styles before that
    head_loc = html.index("</head>")
    new_html = "{}{}{}".format(
        html[:head_loc], styles_html, html[head_loc:])

    return new_html


def generate_pdf(api_key, html, callback, **kwargs):
    # First get HTML string to use
    if html is None:
        callback(error='No HTML found.')
        return

    if api_key is None:
        callback(error='No API key found.')
        return

    filename = 'example'
    if 'filename' in kwargs:
        filename = kwargs['filename']

    if 'build_toc' in kwargs:
        html = build_toc(html)

    is_test = True
    if 'is_production' in kwargs:
        is_test = False

    if 'include_default_styles' in kwargs:
        html = insert_default_styles(html)

    # Save intermediate html output to outbox
    with open('outbox/{}.html'.format(filename), 'w') as fh:
        fh.write(html)

    # Init the docraptor
    docraptor.configuration.username = api_key
    doc_api = docraptor.DocApi()

    print("Converting file \"{}\"...".format(filename))

    # Variables for tracking generation time
    time_counter = 0
    sleep_increment = 0.1  # in seconds

    try:
        create_response = doc_api.create_async_doc({
            "test": is_test,     # test documents are free but watermarked
            "document_content": html,           # supply content directly
            "name": "{}.pdf".format(filename),  # help find document later
            "document_type": "pdf",             # pdf or xls or xlsx
            "prince_options": {
                "javascript": True              # generated content in js
                # 'baseurl': 'https://s3.amazonaws.com'
            }
        })

        while True:
            status_response = doc_api.get_async_doc_status(create_response.status_id)
            if status_response.status == "completed":
                doc_response = doc_api.get_async_doc(status_response.download_id)
                duration = time_counter * sleep_increment * 1000
                kwargs = {}
                kwargs['filename'] = filename
                kwargs['doc_response'] = doc_response
                callback(duration=duration, **kwargs)
                break
            elif status_response.status == "failed":
                callback(error="failed")
                break
            else:
                time_counter += 1
                time.sleep(sleep_increment)

    except docraptor.rest.ApiException as error:
        callback(error=error)
