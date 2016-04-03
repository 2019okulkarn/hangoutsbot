import plugins
from control import *
from admin import is_admin
from collections import Counter


def _initialize():
    plugins.register_user_command(["poll"])


def add(bot, name):
    if not bot.memory.exists(["polls"]):
        bot.memory.set_by_path(["polls"], {})
    if not bot.memory.exists(["polls", name]):
        bot.memory.set_by_path(["polls", name], {})
        bot.memory.save()
        msg = _("Poll '{}' created").format(name)
    else:
        msg = _("Poll '{}' already exists").format(name)
    return msg


def delete(bot, name):
    path = bot.memory.get_by_path(['polls'])
    if name in path:
        del path[name]
        bot.memory.set_by_path(['polls'], path)
        bot.memory.save()
        msg = _('Poll "{}"" deleted.').format(name)
    else:
        msg = _('There is no poll by the name "{}"').format(name)
    return msg


def vote(bot, event, vote_, name, pollnum):
    mem = bot.memory
    path = mem.get_by_path(["polls"])
    names = []
    for poll in path:
        names.append(poll)
    if pollnum == -1:
        poll = name
    else:
        if len(names) >= pollnum:
            poll = names[pollnum]
        else:
            poll = name
    path = bot.memory.get_by_path(["polls", poll])
    path[event.user.first_name] = vote_.lower()
    bot.memory.set_by_path(['polls', poll], path)
    bot.memory.save()
    msg = _('Your vote for {} has been recorded as {}').format(poll, vote_)
    return msg


def set_help(bot, pollnum, help_text):
    mem = bot.memory
    path = mem.get_by_path(["polls"])
    names = []
    for poll in path:
        names.append(poll)
    if len(names) >= pollnum:
        poll = names[pollnum]
    path = bot.memory.get_by_path(["polls", poll])
    path["help"] = help_text
    bot.memory.set_by_path(['polls', poll], path)
    bot.memory.save()
    return "Help for <b>{}</b> set to '{}'".format(poll, help_text)


def get_help(bot, name, pollnum):
    mem = bot.memory
    path = mem.get_by_path(["polls"])
    names = []
    for poll in path:
        names.append(poll)
    if pollnum == -1:
        poll = name
    else:
        if len(names) >= pollnum:
            poll = names[pollnum]
        else:
            poll = name
    if bot.memory.exists(["polls", poll, "help"]):
        help_text = bot.memory.get_by_path(["polls", poll, "help"])
    else:
        help_text = "None"
    return "Help for <b>{}:</b>\n{}".format(poll, str(help_text))


def results(bot, poll):
    votes = []
    names = []
    mesg = []
    winners = []
    path = bot.memory.get_by_path(["polls", poll])
    for person in path:
        names.append(person)
        vote = path[person]
        votes.append(vote)
    for i in range(len(names)):
        result = '{} voted {}<br>'.format(names[i], votes[i])
        mesg.append(result)
    count = Counter(votes)
    freqlist = []
    for item in count:
        freqlist.append(item)
    maxcount = max(freqlist)
    total = freqlist.count(maxcount)
    common = count.most_common(total)
    for item in common:
        winners.append(str(item[0]))
    freq = str(common[0][1])
    if len(winners) == 1:
        mesg.append(
            '<br>THE WINNER IS <b>{}</b> with <b>{}</b> votes'.format(winners[0], freq))
    else:
        mesg.append(
            '<br>THE WINNERS ARE <b>{}</b> with <b>{}</b> votes'.format(', '.join(winners), freq))
    msg = ''.join(mesg)
    return msg


def list(bot):
    path = bot.memory.get_by_path(['polls'])
    polls = []
    for poll in path:
        polls.append('•' + poll)
    if len(polls) == 0:
        msg = _('No polls exist right now.')
    else:
        msg = '<br>'.join(polls)
    return msg


def submit_for_approval(bot, event):
    if not bot.memory.exists(["requests"]):
        bot.memory.set_by_path(["requests"], {})
        bot.memory.save()
    if not bot.memory.exists(["requests", "polls"]):
        bot.memory.set_by_path(["requests", "polls"], {})
        bot.memory.save()
    path = bot.memory.get_by_path(["requests", "polls"])
    requestnum = len(path) + 1
    text = str(event.conv_id) + " " + event.text
    bot.memory.set_by_path(["requests", "polls", str(requestnum)], text)
    bot.memory.save()
    return ["Poll request {} submitted for approval".format(requestnum), "New poll requested by {} -- {}\nTo approve this poll, do ! approve poll {}".format(event.user.first_name, event.text, requestnum)]


def poll(bot, event, *args):
    '''Creates a poll. Format is /bot poll [--add, --delete, --list, --vote] [pollnum, pollname] [vote]'''
    if args:
        if args[0] == '--add' and is_admin(bot, event):
            if len(args) > 1:
                name = ' '.join(args[1:])
                msg = add(bot, name)
        elif args[0] == '--add' and not is_admin(bot, event):
            request = submit_for_approval(bot, event)
            msg = request[0]
            yield from bot.coro_send_message(CONTROL, _(request[1]))
            #msg = _("{}: Can't do that.").format(event.user.full_name)
        elif args[0] == '--delete' and is_admin(bot, event):
            name = ' '.join(args[1:])
            msg = delete(bot, name)
        elif args[0] == '--delete' and not is_admin(bot, event):
            msg = _("{}: Can't do that.").format(event.user.full_name)
        elif args[0] == '--vote':
            if args[1].isdigit():
                pollnum = int(args[1]) - 1
                msg = vote(bot, event, ' '.join(args[2:]), "default", pollnum)
            else:
                vote_ = ' '.join(args[1:]).split(' - ')[0]
                name = ' '.join(args[1:]).split(' - ')[1]
                msg = vote(bot, event, vote_, name, -1)
        elif args[0] == '--list':
            msg = list(bot)
        elif args[0] == '--results':
            if args[1].isdigit():
                path = bot.memory.get_by_path(['polls'])
                pollnum = int(args[1]) - 1
                keys = []
                for poll in path:
                    keys.append(poll)
                if len(keys) > 0 and len(keys) >= pollnum:
                    poll = keys[pollnum]
                    msg = results(bot, poll)
                else:
                    msg = _("Not that many polls")
            else:
                poll = ' '.join(args[1:])
                msg = results(bot, poll)
        elif args[0] == '--help':
            if args[1] == '--set' and is_admin(bot, event):
                if args[2].isdigit():
                    pollnum = int(args[2]) - 1
                    msg = set_help(bot, pollnum, ' '.join(args[3:]))
                else:
                    msg = _("What number poll do you want to add help for?")
            elif args[1] == '--set' and not is_admin(bot, event):
                request = submit_for_approval(bot, event)
                msg = request[0]
                yield from bot.coro_send_message(CONTROL, _(request[1]))
            else:
                if args[1].isdigit():
                    pollnum = int(args[1]) - 1
                    msg = get_help(bot, "default", pollnum)
                else:
                    msg = get_help(bot, ' '.join(args[1:]), -1)
        else:
            if args[0].isdigit():
                pollnum = int(args[0]) - 1
                msg = vote(bot, event, ' '.join(args[1:]), "default", pollnum)
            else:
                vote_ = ' '.join(args).split(' - ')[0]
                name = ' '.join(args).split(' - ')[1]
                msg = vote(bot, event, vote_, name, -1)
    else:
        msg = _(
            "Creates a poll. Format is /bot poll [--add, --delete, --list, --vote, --results] [pollnum, pollname] [vote]")
    yield from bot.coro_send_message(event.conv, msg)
    bot.memory.save()
