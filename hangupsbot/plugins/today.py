import plugins
from bs4 import BeautifulSoup as Soup
from requests import get

def _initialize():
    plugins.register_user_command(["today"])

def today(bot, event, *args):
    r = get("http://www.nationaldaycalendar.com/feed/")
    soup = Soup(r.text, "lxml")
    day = soup.item.title.string.title()
    yield from bot.coro_send_message(event.conv, _(day)) 
