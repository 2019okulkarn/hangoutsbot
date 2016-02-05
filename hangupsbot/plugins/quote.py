import asyncio, logging, re

from random import choice
import time
import plugins
from control import *

logger = logging.getLogger(__name__)

def _initialize():
    plugins.register_admin_command(["addquote"])
    plugins.register_user_command(["quote"])

def addquote(bot, event, *args):
    '''Adds a quote to the bot's memory. Format is /bot addquote <quote> - <person>'''
    try:
        if args:
            quote = ' '.join(args).split(' - ')
            user = quote[1].lower()
            if not bot.memory.exists([user]):
                bot.memory.set_by_path([user], {})
            quotemem = bot.memory.get_by_path([user])
            quotetoadd = quote[0]
            quotemem[str(time.time())] = quotetoadd
            bot.memory.set_by_path([user], quotemem)
            bot.memory.save()
            msg = _("New quote for {}").format(user)
        else:
            msg = _("Please give me a quote to add")
        yield from bot.coro_send_message(event.conv, msg)
        bot.memory.save()
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROL, msg)

def quote(bot, event, *args):
    '''Retrieves quote from bot's memory. Format is /bot quote <person>'''
    try:
        if args:
            user = ' '.join(args).lower()
            listofquotes = bot.memory.get_by_path([user])
            if ',' in str(listofquotes):
                quotelist = str(listofquotes).split(',')
                chosenquote = choice(quotelist)
                chosenquotelist = chosenquote.split(':')
                quotetoshow = chosenquotelist[1]
                quotecheck = list(quotetoshow)
                for i in range(len(quotecheck)):
                    if quotecheck[i] == '}':
                        quotecheck[i] = ''
                    else:
                        quotecheck[i] = quotecheck[i]
                quote = ''.join(quotecheck)
                msg = _("{} - {}").format(quote, user)
            else:
                quotelist = str(listofquotes).split(':')
                quotetoshow = quotelist[1]
                quotecheck = list(quotetoshow)
                for i in range(len(quotecheck)):
                    if quotecheck[i] == '}':
                        quotecheck[i] = ''
                    else:
                        quotecheck[i] = quotecheck[i]
                quote = ''.join(quotecheck)
                msg = _("{} - {}").format(quote, user)
        else:
            msg = _("Incorrect number of arguments")
    except:
        msg = _("No quote found")
    yield from bot.coro_send_message(event.conv, msg)


