import re, json, logging

import hangups

import plugins

from utils import *

from commands import command

def _initialise():
    plugins.register_user_command(["celebrate"])

def celebrate(bot, event, *args):
    '''Celebrate something. Format is /bot celebrate <what you want to celebrate>'''
    if args:
        msg = _(" .--.<br>;    ;<br>  '..'<br>  \\<br>  / <br><b><i>WOOHOO {}!!!").format(' '.join(args).upper())
        yield from bot.coro_send_message(event.conv.id_, msg)
    else:
        msg = _(" .--.<br>;    ;<br> '..'<br>    \\<br>    / <br><b><i>WOOHOO!!!")
        yield from bot.coro_send_message(event.conv.id_, msg)
