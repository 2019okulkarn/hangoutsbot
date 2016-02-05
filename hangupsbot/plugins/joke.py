from urllib.request import urlopen
import plugins
from control import *
def _initialize():
    plugins.register_user_command(['joke'])

def joke(bot, event, *args):
    '''Tells a joke from http://tambal.azurewebsites.net/joke/random Format is /bot joke'''
    try:
        request = urlopen('http://tambal.azurewebsites.net/joke/random')
        json = request.read()
        jsonlist = list(json)
        jsonlist = [chr(x) for x in jsonlist]
        json = ''.join(jsonlist)
        attr = json.split(':')
        unix = attr[1]
        unix = unix.strip('"')
        unixlist = list(unix)
        unixlist[-1] = ''
        unixlist[-2] = ''
        unix = ''.join(unixlist)
        joke = unix
        if len(args) == 0:
            msg = _('{}').format(joke)
        else:
            msg = _('<i>Too many parameters')
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROl, msg)
