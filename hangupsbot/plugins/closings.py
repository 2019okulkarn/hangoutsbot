import plugins
import json
from requests import get
from control import *

def _initialise():
    plugins.register_user_command(['fcps'])

def fcps(bot, event, *args):
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