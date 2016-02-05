import plugins
from slogans import slogans
from random import choice
from control import *
def _initialise():
    plugins.register_user_command(['slogan'])

def slogan(bot, event, *args):
    '''Creates a slogan for something. Format is /bot slogan <something>''' 
    try:
        slogan = choice(slogans).format(' '.join(args))
        msg = _('{}').format(slogan)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        simple = _('An Error Occurred. Sorry About That.')
        msg = ('{}').format(str(e))
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)
