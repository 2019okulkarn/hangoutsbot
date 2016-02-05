import plugins

def _initialise():
    plugins.register_user_command(["congratulate"])

def congratulate(bot, event, *args):
    '''Congratulate somebody/something. The correct format is /bot congratulate <what to congratulate>'''
    if args:
        tbc = ' '.join(args).upper()
        msg = _("CONGRATS {}!!!!!!!!!!!<br>👏👏👏👏👏👏👏👏👏👏👏👏👏👏👏👏👏👏").format(tbc)
    else:
        msg = _("Who do I congratulate?")
    yield from bot.coro_send_message(event.conv, msg)
    
