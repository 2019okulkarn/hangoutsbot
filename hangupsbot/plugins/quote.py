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

def retrieve(conn, id):
	c = conn.cursor()
	c.execute('SELECT * FROM quotes WHERE id = ?', [id])
	quote = c.fetchone()
	msg = str(quote)
	return msg

def quote(bot, event, *args):
	conn = sqlite3.connect('bot.db')
	msg = _(retrieve(conn, args[0]))
	yield from bot.coro_send_message(event.conv, msg)
	conn.close()

def delete(conn, id):
	pass

def edit(conn, id, quote):
	pass

def quote(bot, event, *args):
	try:
		conn = sqlite3.connect('bot.db')
		if args[0] not in ['-a', '-d', '-l', '-e'] and args[0].startswith('-'):
			msg = _("Invalid Flag")
			yield from bot.coro_send_message(event.conv, msg)
		elif args[0] in ['-a', '-d', '-e'] and is_admin(bot, event): # admin only quote functions
			if args[0] == "-a":
				text = " ".join(args[1:]).split(' - ')
				add(conn, text[1], text[2])
				msg = _("Sucessfully added quote!")
			elif args[0] == "-d":
				delete(conn, args[1])
			elif args[0] == "-e":
				edit(conn, args[1], " ".join(args[2:]))
		elif not is_admin(bot, event):
			msg = _("You're not an admin!")
			yield from bot.coro_send_message(event.conv, msg)
		else:
			if " ".join(args).isnumeric():
				retrieve_author()
			yield from bot.coro_send_message(event.conv, msg)
		conn.close()
	except BaseException as e:
		msg = _('{} -- {}').format(str(e), event.text)
		yield from bot.coro_send_message(CONTROL, msg)