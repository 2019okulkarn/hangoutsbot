import plugins
import sqlite3
from control import *
from admin import is_admin, is_tag
from ixio import ixio


def _initialise():
	plugins.register_user_command('quote')
	conn = sqlite3.connect('bot.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS quotes (author TEXT, quote TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)")
	conn.commit()
	conn.close()


def add(conn, quote, author):
	c = conn.cursor()
	c.execute(
    "INSERT INTO quotes(author, quote) VALUES (?, ?)", [
        author.lower(), quote])
	conn.commit()
	msg = "Successfully added quote!"
	return msg


def retrieve(conn, id_, author, full=True):
	c = conn.cursor()
	if not id_:
		c.execute('SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1')
		q = c.fetchone()
		msg = format_quote(q)
	elif not author:
		c.execute('SELECT * FROM quotes WHERE id = ?', [id_])
		q = c.fetchone()
		msg = format_quote(q)
	elif author:
		if not full:
			c.execute(
    'SELECT * FROM quotes WHERE author = ? ORDER BY RANDOM() LIMIT 1',
     [id_])
			q = c.fetchone()
			msg = format_quote(q)
		else:
			c.execute('SELECT * FROM quotes WHERE author = ?', [id_])
			q = c.fetchall()
			quotes = []
			for i in q:
				quotes.append(format_quote(i))
				msg = '\n'.join(quotes)
	return msg


def delete(conn, id_):
	c = conn.cursor()
	c.execute("DELETE from quotes where id=?", [id_])
	conn.commit()


def edit(conn, id_, quote):
	c = conn.cursor()
	c.execute("SELECT * from quotes where id=?", [id_])
	if c.fetchone():
		c.execute("UPDATE quotes SET quote=? WHERE id=?", [quote, id_])
		msg = "Successfully edited quote {}".format(id_)
	else:
		msg = "No such quote."
	conn.commit()
	return msg


def format_quote(q):
	 quote = "Quote {}: {} - {}".format(q[2], q[1], q[0])
	 return quote


def quote(bot, event, *args):
	try:
		conn = sqlite3.connect('bot.db')

		if not args:
			msg = retrieve(conn, None, False)
		elif args[0] not in ['-a', '-d', '-l', '-e'] and args[0].startswith('-'):
			msg = "Invalid Flag"
		elif args[0] in ['-a', '-d', '-e']:
			if len(args) < 2:
				msg = "You're missing arguments!"
			elif is_admin(bot, event) or is_tag(bot, event, 'quote-admin'):  # admin only quote functions
				if args[0] == "-a":  # edit quotes
					text = " ".join(args[1:]).split(' - ')
					if event.user.first_name.lower() == text[1]:
						msg = "You can't submit your own quote!"  # self-submission
					else:
						msg = add(conn, text[0], text[1])
				elif args[0] == "-d":  # delete quotes
					delete(conn, args[1])
					msg = "Successfully deleted quote"
				elif args[0] == "-e":  # edit quotes
					msg = edit(conn, args[1], " ".join(args[2:]))
			else:
				msg = "You're not an admin!"
		elif args[0].startswith('-l'):  # list quotes from author
			msg = str(retrieve(conn, args[1], True))
		else:
			text = " ".join(args)
			author = True if not text.isnumeric() else False
			msg = retrieve(conn, text, author, full=False)
		if len(msg.split('<br>')) >= 4:
			ixio(msg)
		else:
			yield from bot.coro_send_message(event.conv, msg)
		conn.close()
	except TypeError:
		msg = 'No such quote'
		yield from bot.coro_send_message(event.conv, msg)
	except BaseException as e:
		msg = ('{} -- {}').format(str(e), event.text
		yield from bot.coro_send_message(CONTROL, msg)
