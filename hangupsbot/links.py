from bs4 import BeautifulSoup as BS
from urllib.request import urlopen
from requests import get
import json
from urllib.parse import quote

def shorten(url):
    try:
        response = urlopen('http://tinyurl.com/api-create.php?url=' + url)
        html = response.read()
        soup = BS(html, 'html.parser')
        return soup.get_text()
    except:
        error = "Could not create shortened link"
        return error

def get_title(url):
    try:
        response = urlopen(url)
        html = response.read()
        soup = BS(html, 'html.parser')
        return soup.title.string
    except:
        error = "Title not Found"
        return error

def lengthen(url):
    tolengthen = quote(url)
    r = get('http://api.longurl.org/v2/expand?format=json&url=' + tolengthen)
    data = json.loads(r.text)
    return data["long-url"]
