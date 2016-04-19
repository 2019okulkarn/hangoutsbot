import plugins
from admin import is_admin
from plugins.default import get_name

def _initialize():
    plugins.register_user_command(["nick"])


def create_memory(bot, user_id):
    check = bot.user_memory_get(user_id, "nicknames")
    if not check:
        bot.user_memory_set(user_id, "nicknames", [])
        bot.memory.save()
        return True
    else:
        return False


def add_nickname(bot, event, user_id, nickname):
    create_memory(bot, user_id)
    mem = bot.user_memory_get(user_id, "nicknames")
    if not nickname in mem:
        mem.append(nickname)
        bot.user_memory_set(user_id, "nicknames", mem)
        return "Added nickname {} for {}".format(nickname, get_name(bot, user_id))
    else:
        return "Nickname {} already exists for {}".format(nickname, get_name(bot, user_id))


def nick(bot, event, *args):
    '''Adds a nickname. Format is /bot nick <nickname>'''
    if len(args) == 1:
        added = add_nickname(bot, event, event.user.id_.chat_id, args[0].lower())
        if added:
            yield from bot.coro_send_message(event.conv, _(added))
    elif len(args) == 3 and is_admin(bot, event) and args[0] == '--set':
        added = add_nickname(bot, event, args[1], args[2].lower())
        if added:
            yield from bot.coro_send_message(event.conv, _(added))
    else:
        yield from bot.coro_send_message(event.conv, _("Too many args"))
