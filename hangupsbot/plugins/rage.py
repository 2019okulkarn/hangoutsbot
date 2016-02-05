import re, json, logging

import hangups

import plugins

from utils import *

from commands import command

def _initialise():
    plugins.register_user_command(["rage"])

def rage(bot, event, *args):
    '''Rages at something. Format is /bot rage <something>'''
    if args:
        msg = _('<b><i><u>{}!!!').format(' '.join(args).upper())
        yield from bot.coro_send_message(event.conv.id_, msg)
    else:
        msg = _("I can't rage at nothing...")
        yield from bot.coro_send_message(event.conv.id_, msg)
