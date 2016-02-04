import plugins
import json
from requests import get
from control import *
from bs4 import BeautifulSoup

def _initialise():
    plugins.register_user_command(['fcps', 'lcps'])


def lcps(bot, event, *args):
    '''This command checks for school closings in the Loudon County Public Schools area. Data taken from NBC.'''    
    try:
        r = get('http://www.nbcwashington.com/weather/school-closings/')
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        schools = []
        for school in soup.find_all('p'):
            schools.append(school.text)

        for i in range(len(schools)):
            if 'Loudoun County' in schools[i]:
                check = str(schools[i])
        status = check.replace('Loudoun County Schools', '')
        msg = _('LCPS is {}').format(status)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        simple = _('An Error Occurred')
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)

def fcps(bot, event, *args):
    '''This command checks for closings in the Fairfax County Public Schools Area. Data taken from TJHSST.'''
    try:
        page = get('https://ion.tjhsst.edu/api/emerg?format=json')
        data = json.loads(page.text)
        status = data['status']
        if status:
            message = data['message']
            message = message.replace('<p>', '')
            message = message.replace('</p>', '')
            msg = _(message)
        else:
            msg = _('FCPS is open')
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        simple = _('An Error Occurred')
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)
