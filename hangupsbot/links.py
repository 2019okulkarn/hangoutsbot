<<<<<<< HEAD
=======
import json
from urllib.parse import quote
import re
from lxml.html import document_fromstring
from requests import exceptions, get, post


>>>>>>> 933ad2193339b634df2ec1e476aa36886321c6ac
def shorten(url):
    return

<<<<<<< HEAD
def get_title(url):
    return
=======
# Code for get_title is borrowed from http://github.com/tjcsl/cslbot/


def get_title(url):
    title = 'No Title Found'
    # User-Agent is really hard to get right :(
    headers = {'User-Agent': 'Mozilla/5.0 HangoutsBot'}
    req = get(url, headers=headers)
    ctype = req.headers.get('Content-Type')
    if req.status_code != 200:
        title = 'HTTP Error %d: %s' % (req.status_code, req.reason)
    elif ctype is not None and ctype.startswith('image/'):
        title = 'Image'
    else:
        html = document_fromstring(req.content)
        t = html.find('.//title')
        # FIXME: is there a cleaner way to do this?
        if t is not None and t.text is not None:
            # Try to handle multiple types of unicode.
            try:
                title = bytes(map(ord, t.text)).decode('utf-8')
            except (UnicodeDecodeError, ValueError):
                title = t.text
                title = ' '.join(title.splitlines()).strip()
        # If we have no <title> element, but we have a Content-Type, fall back
        # to that
        elif ctype is not None:
            title = ctype
        else:
            title = "Title Not Found"
    return title

>>>>>>> 933ad2193339b634df2ec1e476aa36886321c6ac

def lengthen(url):
    return
