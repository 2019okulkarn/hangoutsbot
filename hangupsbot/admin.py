def is_admin(bot, event, other=None):
    admins_list = bot.get_config_suboption(event.conv_id, 'admins')
    if event.user_id.chat_id in admins_list:
        return True
    else:
        return False


def is_tag(bot, event, tag=None):
    tags = bot.user_memory_get(event.user.id_.chat_id, 'tags')
    if tags:
        if tag in tags:
            return True
        else:
            return False
    else:
        return False
