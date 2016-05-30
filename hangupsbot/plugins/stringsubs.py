import plugins
import re

def _initialise():
    plugins.register_user_command(["oodle", "boaty"])


def oodle(bot, event, *args):
    '''Replaces vowels with 'oodle'; Format is /bot oodle <string>'''
    if args:
        s = " ".join(args)
        r = re.compile(r'[aeiou]', re.IGNORECASE)
        oodled = re.sub(r, 'oodle', s)
        msg = _("{}").format(oodled)
    else:
        msg = _("What should I oodle?")
    yield from bot.coro_send_message(event.conv, msg)


def boaty(bot, event, *args):
    '''Converts message to 'Boaty McBoatface form. Format is /bot boaty <message>'''
    if args:
        boaty = "".join(args)
        msg = _("{}y Mc{}face").format(boaty.title(), boaty.title())
    else:
        msg = _("What should I boaty?")
    yield from bot.coro_send_message(event.conv, msg)
