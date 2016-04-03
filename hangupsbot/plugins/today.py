import plugins
from commands import command
from bs4 import BeautifulSoup as Soup
from requests import get

def _initialize():
    plugins.register_user_command(["today"])

def today(bot, event, *args):
    r = get("http://www.nationaldaycalendar.com/feed/")
    soup = Soup(r.text, "lxml")
    day = soup.item.title.string
    cmd = ["topic", "{} | http://i.okulkarni.cf/Rules.jpg".format(day)]
    yield from command.run(bot, event, *cmd)
