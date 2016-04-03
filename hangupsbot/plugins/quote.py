import plugins
import sqlite3
from control import *
from admin import is_admin


def _initialise():
    plugins.register_user_command('quote')
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS quotes (author TEXT, quote TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)")
    conn.commit()
    conn.close()


def add(conn, quote, author):
    c = conn.cursor()
    c.execute(
        "INSERT INTO quotes(author, quote) VALUES (?, ?)", [
            author, quote])
    conn.commit()


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
    c.execute("UPDATE quotes SET quote=? WHERE id=?", [quote, id_])
    conn.commit()


def format_quote(q):
    quote = "Quote {}: {} - {}".format(q[2], q[1], q[0])
    return quote


def quote(bot, event, *args):
    try:
        conn = sqlite3.connect('bot.db')
        if not args:
            msg = _(retrieve(conn, None, False))
        elif args[0] not in ['-a', '-d', '-l', '-e'] and args[0].startswith('-'):
            msg = _("Invalid Flag")
        elif args[0] in ['-a', '-d', '-e']:
            if is_admin(bot, event):  # admin only quote functions
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
            msg = _(str(retrieve(conn, args[1], True)))
        else:
            text = " ".join(args)
            author = True if not text.isnumeric() else False
            msg = _(retrieve(conn, text, author, full=False))
        yield from bot.coro_send_message(event.conv, msg)
        conn.close()
    except TypeError:
        msg = _('No such quote')
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROL, msg)
        raise e
