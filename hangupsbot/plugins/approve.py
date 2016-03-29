import plugins
from commands import command

def _initialize():
    plugins.register_admin_command(['approve'])

def approve(bot, event, *args):
    request = args[0]
    request_number = str(args[1])
    if request.lower() == 'poll':
        if not bot.memory.exists(["requests"]):
            yield from bot.coro_send_message(event.conv, _("No requests"))
            return
        else:
            path = bot.memory.get_by_path(["requests", "polls", str(request_number)])
            conversation_id = path.split()[0]
            command_to_run = path.split()[2:]
            yield from command.run(bot, event, *command_to_run)
            yield from bot.coro_send_message(conversation_id, _("Poll {} approved").format(request_number))
            return
        return
    else:
        yield from bot.coro_send_message(event.conv, _("Approval for that not yet supported"))
