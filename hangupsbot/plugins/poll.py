import plugins
from control import *
from admin import is_admin
from collections import Counter


def _initialize():
    plugins.register_user_command(["poll"])


def poll(bot, event, *args):
    '''Creates a poll. Format is /bot poll [--add, --delete, --list, --vote] [pollnum, pollname] [vote]'''
    try:
        if args:
            if args[0] == '--add' and is_admin(bot, event):
                if not bot.memory.exists(['polls']):
                    bot.memory.set_by_path(['polls'], {})
                if len(args) > 1:
                    name = ' '.join(args[1:])
                    if not bot.memory.exists(['polls', name]):
                        bot.memory.set_by_path(['polls', name], {})
                        bot.memory.save()
                        msg = _("Poll '{}' created").format(name)
                    else:
                        msg = _("Poll '{}' already exists").format(name)
                else:
                    msg = _("What is this poll called?")
            elif args[0] == '--add' and not is_admin(bot, event):
                msg = _("{}: Can't do that.").format(event.user.full_name)
            elif args[0] == '--delete' and is_admin(bot, event):
                name = ' '.join(args[1:])
                path = bot.memory.get_by_path(['polls'])
                if name in path:
                    del path[name]
                    bot.memory.set_by_path(['polls'], path)
                    bot.memory.save()
                    msg = _('Poll "{}"" deleted.').format(name)
                else:
                    msg = _('There is no poll by the name "{}"').format(name)
            elif args[0] == '--delete' and not is_admin(bot, event):
                msg = _("{}: Can't do that.").format(event.user.full_name)
            elif args[0] == '--vote':
                if not args[1].isdigit():
                    spl = ' '.join(args[1:]).split(' - ')
                    if len(spl) == 2:
                        vote = str(spl[0]).lower()
                        poll = spl[1]
                        path = bot.memory.get_by_path(['polls', poll])
                        path[event.user.first_name] = vote
                        bot.memory.set_by_path(['polls', poll], path)
                        bot.memory.save()
                        msg = _('Your vote for {} has been recorded as {}').format(poll, vote)
                    else:
                        msg = _("The correct format is /bot poll --vote <poll> - <vote> OR /bot poll --vote <pollnum> <vote>")
                else:
                    path = bot.memory.get_by_path(['polls'])
                    pollnum = int(args[1]) - 1
                    if len(list(path.keys())) > 0 and len(list(path.keys())) >= pollnum:
                        polltovote = list(path.keys())[pollnum]
                        vote = ' '.join(args[2:])
                        pollpath = bot.memory.get_by_path(['polls', polltovote])
                        pollpath[event.user.first_name] = vote
                        bot.memory.set_by_path(['polls', polltovote], pollpath)
                        bot.memory.save()
                        msg = _('Your vote for {} has been recorded as {}').format(list(path.keys())[pollnum], vote)
                    else:
                        msg = _("There are not that many polls")
            elif args[0] == '--list':
                path = bot.memory.get_by_path(['polls'])
                polls = []
                for poll in path:
                    polls.append('•' + poll)
                if len(polls) == 0:
                    msg = _('No polls exist right now.')
                else:
                    msg = '<br>'.join(polls)
            #FIXME: Same code is written twice
            elif args[0] == '--results':
                if args[1].isdigit():
                    path = bot.memory.get_by_path(['polls'])
                    pollnum = int(args[1]) - 1
                    if len(list(path.keys())) > 0 and len(list(path.keys())) >= pollnum:
                        poll = list(path.keys())[pollnum]
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
                        freqlist = list(count.values())
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
                    else:
                        msg = _("That poll does not exist")
                else:
                    poll = ' '.join(args[1:])
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
                    freqlist = list(count.values())
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
            else:
                msg = _("Creates a poll. Format is /bot poll [--add, --delete, --list, --vote, --results] [pollnum, pollname] [vote]")
        else:
            msg = _("Creates a poll. Format is /bot poll [--add, --delete, --list, --vote, --results] [pollnum, pollname] [vote]")
        yield from bot.coro_send_message(event.conv, msg)
        bot.memory.save()
    except BaseException as e:
        simple = _('An Error Occurred')
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)
