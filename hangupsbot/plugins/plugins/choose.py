import re, json, logging

import hangups

import plugins
from random import choice
from utils import text_to_segments, simple_parse_to_segments, remove_accents
from commands import command


logger = logging.getLogger(__name__)

def _initialise():
    plugins.register_user_command(["choose"])

def choose(bot, event, *args):
    if len(args) > 1:
        listchoices=' '.join(args).split(' or ')
        chosen = choice(listchoices)
        while chosen == ' or ':
            chosen = choice(listchoices)
        action = ['draws a slip of paper from a hat and gets...', 'says eenie, menie, miney, moe and chooses...','picks a random number and gets...', 'rolls dice and gets...', 'asks a random person and gets...','plays rock, paper, scissors, lizard, spock and gets...']
        chosenaction = choice(action)
        msg = _("{} {}").format(chosenaction,chosen)
    else:
        msg = _("Give me at least 2 things to choose from")
    yield from bot.coro_send_message(event.conv, msg)

