import plugins
import sqlite3
from control import *
from admin import is_admin

def _initialise():
	plugins.register_user_command('quote')
	conn = sqlite3.connect('bot.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS  quotes (author TEXT, quote TEXT,  id INTEGER PRIMARY KEY AUTOINCREMENT)")
	conn.commit()
	conn.close()

def add(conn, quote, author):
	c = conn.cursor()
	c.execute("INSERT INTO quotes(quote, author) VALUES (?, ?)", [author, quote])
	conn.commit()

def retrieve(conn, id_, author, full=True):
	c = conn.cursor()
	if not author:
		c.execute('SELECT * FROM quotes WHERE id = ?', [id_])
		quote = c.fetchone()
		msg = str(quote)
	elif author:
		c.execute('SELECT * FROM quotes WHERE author = ?', [id_])
		quote = c.fetchall() if full else c.fetchone()
		msg = str(quote)
	return msg

def delete(conn, id):
	pass

def edit(conn, id, quote):
	pass

def quote(bot, event, *args):
	if not args:
		msg = _("Please give me some args!")
		yield from bot.coro_send_message(event.conv, msg)
		return
	try:
		conn = sqlite3.connect('bot.db')
		if args[0] not in ['-a', '-d', '-l', '-e'] and args[0].startswith('-'):
			msg = _("Invalid Flag")
		elif args[0] in ['-a', '-d', '-e']:
			if is_admin(bot, event): # admin only quote functions
				if args[0] == "-a":
					text = " ".join(args[1:]).split(' - ')
					add(conn, text[0], text[1])
					msg = _("Successfully added quote")
				elif args[0] == "-d":
					delete(conn, args[1])
					msg = _("Successfully deleted quote")
				elif args[0] == "-e":
					edit(conn, args[1], " ".join(args[2:]))
					msg = _("Successfully edited quote")
			else:
				msg = _("You're not an admin!")
		elif args[0].startswith('-l'):
			quotes = retrieve(conn, args[1], full=True, author=True)
		else:
			text = " ".join(args)
			author = True if not text.isnumeric() else False
			msg = _(retrieve(conn, text, author))
		yield from bot.coro_send_message(event.conv, msg)
		conn.close()
	except BaseException as e:
		msg = _('{} -- {}').format(str(e), event.text)
		yield from bot.coro_send_message(CONTROL, msg)
		raise e
