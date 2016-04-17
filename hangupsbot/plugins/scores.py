import plugins
import asyncio

def _initialize():
    plugins.register_handler(_listen_for_score, type="message")
    plugins.register_user_command(["score"])

def create_memory(bot, name):
    if not bot.memory.exists(["scores"]):
        bot.memory.set_by_path(["scores"], {})
    if not bot.memory.exists(["scores", name]):
        bot.memory.set_by_path(["scores", name], 0 )
    bot.memory.save()

def increment_score(bot, name, val):
    create_memory(bot, name)
    current_score = bot.memory.get_by_path(["scores", name])
    new_score = current_score + val
    bot.memory.set_by_path(["scores", name], new_score)
    bot.memory.save()

def get_score(bot, name):
    if not bot.memory.exists(["scores", name]):
        return "Nobody cares about {}".format(name.title())
    score = bot.memory.get_by_path(["scores", name])
    return "Score for {}: {}".format(name.title(), score)

def score(bot, event, *args):
    if len(args) == 1:
        name = args[0].lower()
        msg = get_score(bot, name)
    else:
        msg = _("Wrong number of arguments!")
    yield from bot.coro_send_message(event.conv, msg)

@asyncio.coroutine
def _listen_for_score(bot, event, command):
    names_to_add = []
    names_to_subtract = []
    for word in event.text.lower().split():
        if '++' in word:
            name_to_add = word.replace('++', '')
            names_to_add.append(name_to_add)
        if '--' in word:
            name_to_add = word.replace('--', '')
            names_to_subtract.append(name_to_add)
    for name in names_to_add:
        increment_score(bot, name, 1)
    for name in names_to_subtract:
        increment_score(bot, name, -1)
