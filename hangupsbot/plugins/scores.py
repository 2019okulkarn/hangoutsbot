import plugins
import asyncio
from admin import is_admin

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

def set_score(bot, name, val):
    create_memory(bot, name)
    bot.memory.set_by_path(["scores", name], val)
    bot.memory.save()
    return "Set score for {} to {}".format(name.title(), val)

def get_score(bot, name):
    if not bot.memory.exists(["scores", name]):
        return "Nobody cares about {}".format(name.title())
    score = bot.memory.get_by_path(["scores", name])
    return "Score for {}: {}".format(name.title(), score)

def score(bot, event, *args):
    '''Get the score for a user. Format is /bot score <name>
   To increment scores, do <name>++ or <name>--'''
    if len(args) == 1:
        if args[0].lower() == '--high':
            msg = get_high_score(bot)
        elif args[0].lower() == '--low':
            msg = get_low_score(bot)
        else:
            name = args[0].lower()
            msg = get_score(bot, name)
    elif args[0].lower() == '--set' and len(args) == 3 and is_admin(bot, event):
        name = args[1].lower()
        val = args[2].lower()
        msg = set_score(bot, name, int(val))
    else:
        msg = _("Wrong number of arguments!")
    yield from bot.coro_send_message(event.conv, msg)

def get_high_score(bot):
    scores = bot.memory.get_by_path(["scores"])
    inverse = [(value, key) for key, value in scores.items()]
    msg = "{}: {}".format(max(inverse)[1].title(), max(inverse)[0])
    return msg

def get_low_score(bot):
    scores = bot.memory.get_by_path(["scores"])
    inverse = [(value, key) for key, value in scores.items()]
    msg = "{}: {}".format(min(inverse)[1].title(), min(inverse)[0])
    return msg

@asyncio.coroutine
def _listen_for_score(bot, event, command):
    names_to_add = []
    names_to_subtract = []
    for word in event.text.lower().split():
        if word.endswith('++') and not word == '++':
            name_to_add = word.replace('++', '')
            names_to_add.append(name_to_add)
        if word.endswith('--') and not word == '--':
            name_to_add = word.replace('--', '')
            names_to_subtract.append(name_to_add)
    for name in names_to_add:
        if name == event.user.first_name.lower() or name in event.user.full_name.lower():
            increment_score(bot, name, -10)
        else:
            increment_score(bot, name, 1)
    for name in names_to_subtract:
        increment_score(bot, name, -1)
