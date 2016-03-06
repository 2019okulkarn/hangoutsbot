def is_admin(bot, event):
    admins_list = bot.get_config_suboption(event.conv_id, 'admins')
    if event.user_id.chat_id in admins_list:
        return True
    else:
        return False
