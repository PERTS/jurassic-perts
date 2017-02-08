import os
import sys
import urllib
import argparse

import config
from doc_generator import generate_pdf


def callback_function(duration=0, error=None, **kwargs):
    if error:
        print(error)
        return
    filename = 'example'
    if 'filename' in kwargs:
        filename = kwargs['filename']
    if 'doc_response' in kwargs:
        doc_response = kwargs['doc_response']
    file = open("{}/{}.pdf".format(config.outbox_dir, filename), "wb")
    file.write(doc_response)
    file.close
    print("PDF generated at \"{}/{}.pdf\"".format(config.outbox_dir, filename))
    print("PDF generated in ~{}ms".format(duration))


# Arguments to be used by the PDF generation function
kwargs = {}

parser = argparse.ArgumentParser(description='Process some integers.')
# Optional argument
parser.add_argument('api_key', type=str,
                    help='Required string')
# Switch
parser.add_argument('--production', action='store_true',
                    help='A boolean switch')
# Switch
parser.add_argument('--ignore_styles', action='store_true',
                    help='A boolean switch')
args = parser.parse_args()
# Determine testing or production (paid) from arguments
# Default to 'test' because why waste money?
if args.production:
    print('Running script for PRODUCTION')
    kwargs['is_production'] = True
else:
    print('Running script for TESTING')

# Determine if default styles should be embedded or not
# Default to True because our styles are bomb
if args.ignore_styles:
    print('Ignoring awesome pre-built styles...')
else:
    print('Using awesome pre-built styles...')
    kwargs['include_default_styles'] = True

# Determine if Table of Contents should be generated or not
# Default to False because it requires some HTML finess
should_generate_toc = False
if '--toc' in sys.argv:
    should_generate_toc = True
    kwargs['build_toc'] = True

# Loops through all files in the "inbox" folder
for html_file in os.listdir(config.inbox_dir):

    # Determine if file is the correct format
    if html_file.split('.')[1] == 'html':
        kwargs['filename'] = html_file.split('.')[0]
        html = urllib.urlopen("{}/{}".format(
            config.inbox_dir, html_file)).read()       

        print("Converting file \"{}\"...".format(html_file))
        generate_pdf(args.api_key, html, callback_function, **kwargs)

    else:
        print('\"{}\" is not a valid HTML file. Skipping.'.format(html_file))
