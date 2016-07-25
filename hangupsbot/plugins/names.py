import plugins
import re

def _initialise():
    plugins.register_user_command(["oodle", "boaty"])


def oodle(bot, event, *args):
    '''Converts message to yoda speak. Format is /bot yoda <message>'''
    if args:
        s = " ".join(args)
        r = re.compile(r'[aeiou]', re.IGNORECASE)
        oodled = re.sub(r, 'oodle', s)
        msg = _("{}").format(oodled)
    else:
        msg = _("What should I oodle?")
    yield from bot.coro_send_message(event.conv, msg)


def boaty(bot, event, *args):
    '''Converts message to yoda speak. Format is /bot yoda <message>'''
    if args:
        boaty = " ".join(args)
        msg = _("{}y Mc{}face").format(s.title(), s.title())
    else:
        msg = _("What should I boaty?")
    yield from bot.coro_send_message(event.conv, msg)

