import plugins
import re
from links import *

def _initialise():
    plugins.register_handler(_watch_for_link, type="message")

def get_all_urls(text):
    url_regex = re.compile(r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?....]))""")
    return [x[0] for x in url_regex.findall(text)]

@asyncio.coroutine
def _watch_for_link(bot, event, command):
    urls = get_all_urls(event.text)
    for url in urls:
        link = shorten(url)
        title = get_title(url)
        msg = _("** {} **\n{}").format(title, link)
        yield from bot.coro_send_message(event.conv, msg)
