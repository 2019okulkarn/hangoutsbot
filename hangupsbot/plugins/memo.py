import plugins
import asyncio
import datetime


def _initialize():
    plugins.register_handler(_check_if_memo, type="message")
    plugins.register_user_command(["memo"])


def get_id(bot, name):
    all_users = {}
    path = bot.memory.get_by_path(["user_data"])
    for person in path:
        try:
            hangupsuser = bot.get_hangups_user(person)
        except:
            hangupsuser = None
        all_users[person] = hangupsuser
    for user in all_users:
        userdata = all_users[user]
        if name in userdata.full_name.lower():
            return user


def get_name(bot, id_):
    user = bot.get_hangups_user(id_)
    return user.full_name


def create_memory(bot, name):
    user_id = get_id(bot, name)
    if user_id:
        check = bot.user_memory_get(user_id, "memos")
        if not check:
            bot.user_memory_set(user_id, "memos", [])
            return True
        else:
            return False


def add_memo(bot, event, name, text):
    create_memory(bot, name)
    id_ = get_id(bot, name)
    if not id_:
        return "No user by that name"
    else:
        mem = bot.user_memory_get(id_, "memos")
        mem.append('Memo from {}: "{}" at {}'.format(
            event.user.first_name, text, str(datetime.datetime.now())))
        bot.user_memory_set(id_, "memos", mem)
        name = get_name(bot, id_)
        return "Memo added for {}".format(name)


def memo(bot, event, *args):
    '''Leaves a memo for someone. Format is /bot memo <name> <message>'''
    added = add_memo(bot, event, args[0].lower(), ' '.join(args[1:]))
    if added:
        yield from bot.coro_send_message(event.conv, _(added))


@asyncio.coroutine
def _check_if_memo(bot, event, command):
    id_ = event.user.id_.chat_id
    memos = bot.user_memory_get(id_, "memos")
    if memos:
        msg = _('<b>{}:</b>\n{}').format(event.user.first_name, '\n'.join(memos))
        bot.user_memory_set(id_, "memos", [])
        yield from bot.coro_send_message(event.conv, msg)
