import plugins
import sqlite3

def _initialise():
	plugins.register_user_command(['quote', 'addquote'])
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

def addquote(bot, event, *args):
	conn = sqlite3.connect('bot.db')
	add(conn, args[0], args[1])
	msg = _('added fam')
	yield from bot.coro_send_message(event.conv, msg)
	conn.close()