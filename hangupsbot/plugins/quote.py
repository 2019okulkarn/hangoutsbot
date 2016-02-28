<<<<<<< HEAD
=======
import asyncio
import logging
import re

from random import choice
import time
>>>>>>> 933ad2193339b634df2ec1e476aa36886321c6ac
import plugins
import sqlite3

def _initialise():
	plugins.register_admin_command(['quote', 'addquote'])
	conn = sqlite3.connect('bot.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS  quotes (author TEXT, quote TEXT,  id INTEGER PRIMARY KEY AUTOINCREMENT)")
	conn.commit()
	conn.close()

<<<<<<< HEAD
def add(conn, quote, author):
	c = conn.cursor()
	c.execute("INSERT INTO quotes(quote, author) VALUES (?, ?)", [author, quote])
	conn.commit()

def retrieve(conn, id_):
	c = conn.cursor()
	c.execute('SELECT * FROM quotes WHERE id = ?', [id_])
	quote = c.fetchone()
	msg = str(quote)
	return msg
=======

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
>>>>>>> 933ad2193339b634df2ec1e476aa36886321c6ac


def quote(bot, event, *args):
<<<<<<< HEAD
	conn = sqlite3.connect('bot.db')
	msg = _(retrieve(conn, args[0]))
	yield from bot.coro_send_message(event.conv, msg)
	conn.close()

def addquote(bot, event, *args):
	conn = sqlite3.connect('bot.db')
	add(conn, args[0], args[1])
	msg = _('added fam')
	yield from bot.coro_send_message(event.conv, msg)
	conn.close()
=======
    '''Retrieves quote from bot's memory. Format is /bot quote <person>'''
    try:
        if args:
            if args[-1].isdigit():
                user = ' '.join(args[:-1]).lower()
                num = args[-1]
            else:
                user = ' '.join(args).lower()
                num = None
            listofquotes = bot.memory.get_by_path([user])
            if ',' in str(listofquotes):
                quotelist = str(listofquotes).split(',')
                chosenquote = choice(quotelist) if not num else quotelist[num]
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
>>>>>>> 933ad2193339b634df2ec1e476aa36886321c6ac
