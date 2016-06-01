import plugins
from links import *
import asyncio
import re
import requests

def _initialise():
    plugins.register_handler(_reddit_links, type="message")

@asyncio.coroutine
def _reddit_links(bot, event, command):
    matcher = re.compile('(?!https?).*/?r/.*')
    if matcher.match(event.text):
        subreddit = event.text.rsplit('r/')[-1]
        headers = {'User-Agent': 'Mozilla/5.0 HangoutsBot'}
        returned = requests.get('https://reddit.com/r/{}'.format(subreddit), headers=headers)
        if returned.status_code == 200:
            link = 'https://reddit.com/r/{}'.format(subreddit)
            message = _('\*\*{}\*\*\n{}').format(get_title(link), shorten(link))
            yield from bot.coro_send_message(event.conv, message)


