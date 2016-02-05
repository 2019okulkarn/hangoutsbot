import plugins

def _initialise():
    plugins.register_user_command(["vlog"])

def vlog(bot, event, *args):
    '''Sends link to SODA Central Vlogs. Format is /bot vlog'''
    if not args:
        msg = _("** SODA Central Vlogs and More - YouTube ** -- http://tinyurl.com/jzuqj3z")
    else:
        msg = _("Please don't enter any arguments")
    yield from bot.coro_send_message(event.conv, msg)
