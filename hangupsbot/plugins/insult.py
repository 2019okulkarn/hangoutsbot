import plugins, string

from random import choice as choose

from insultslist import *

def _initialise():
    plugins.register_user_command(["insult"])

def insult(bot, event, *args):
    '''Insult something/somebody using a predefined list of insults. Will not insult itself. Format is /bot insult <whattoinsult>'''
    if args:
        insulttouse = choose(insultslist.insults)
        checkforbot = ''.join(args)
        for c in string.punctuation:
            checkforbot = checkforbot.replace(c,'')
        for i in range(len(checkforbot)):
            if not checkforbot[i].isalnum == True:
                checkforbot[i].replace(checkforbot[i], '')
        tobeinsulted = ' '.join(args)
        if '@' in tobeinsulted or '0' in tobeinsulted.lower() or '()' in tobeinsulted.lower() or 'soda' in tobeinsulted.lower() or 'soda' in checkforbot.lower():
            msg = _("I'm not insulting myself")
        elif 's' in tobeinsulted.lower() and 'o' in tobeinsulted.lower() and 'd' in tobeinsulted.lower() and 'a' in tobeinsulted.lower():
            msg = _("I'm not insulting myself")
        else:
            msg = _("Hey {}, {}").format(tobeinsulted, insulttouse)
    else:
        msg = _("I'm not going to insult nobody. They dont' have a life anyways ;)")
    yield from bot.coro_send_message(event.conv, msg)
