import plugins
from comebacks import comebackslist
import random

def _initialise():
    plugins.register_user_command(["comeback"])

def comeback(bot, event, *args):
    '''Bot gives you a comeback. Format is /bot comeback'''
    if not args:
        comeback = random.choice(comebackslist)
        msg = _("A comeback for you because you're not original enough: {}").format(comeback)
    else:
        msg = _("No arguments for comebacks!")
    yield from bot.coro_send_message(event.conv, msg)
