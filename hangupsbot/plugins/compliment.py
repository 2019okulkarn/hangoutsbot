import plugins, string

from random import choice as choose

from complimentslist import *

def _initialise():
    plugins.register_user_command(["compliment"])

def compliment(bot, event, *args):
    '''Compliment something. The correct format is /bot compliment <what to compliment>'''
    if args:
        if 'me' in ''.join(args).lower():
            complimenttouse = choose(compliments)
            tobecomplimented = event.user.first_name
            msg = _("Hey {}, {}").format(tobecomplimented, complimenttouse) 
        elif 'trump' not in ''.join(args).lower():
            complimenttouse = choose(compliments)
            tobecomplimented = ' '.join(args)
            msg = _("Hey {}, {}").format(tobecomplimented, complimenttouse)
        else:
            msg =_("Trump is unable to be complimented")
    else:
        compliment = choose(compliments)
        msg = _("{}").format(compliment)
    yield from bot.coro_send_message(event.conv, msg)
