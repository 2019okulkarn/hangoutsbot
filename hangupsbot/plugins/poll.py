import plugins
from control import *
from collections import Counter

def _initialize():
    plugins.register_admin_command(["poll"])
    plugins.register_user_command(["vote","polls", "results"])

def poll(bot, event, *args):
    '''Creates a poll. Format is /bot poll <name>'''
    try:
        if not bot.memory.exists(['polls']):
                bot.memory.set_by_path(['polls'], {})
        if args:
            name = ' '.join(args)
            bot.memory.set_by_path(['polls', name], {})
            bot.memory.save()
            msg = _("Poll '{}' created").format(name)
        else:
            msg = _("What is this poll called?")
        yield from bot.coro_send_message(event.conv, msg)
        bot.memory.save()
    except BaseException as e:
        simple = _('An Error Occurred')
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)

def polls(bot, event, *args):
    '''Lists available polls. Format is /bot polls.'''
    path = bot.memory.get_by_path(['polls'])
    polls = []
    for poll in path:
        polls.append('•' + poll)
    msg = '<br>'.join(polls)
    yield from bot.coro_send_message(event.conv, msg)

def vote(bot, event, *args):
    '''Votes in a poll. Format is /bot vote <vote> - <poll>'''
    try:
        spl = ' '.join(args).split(' - ')
        if len(spl) == 2:  
            vote = spl[0]
            poll = spl[1]
            path = bot.memory.get_by_path(['polls', poll])
            path[event.user.first_name] = vote
            bot.memory.set_by_path(['polls', poll], path)
            bot.memory.save()
            msg = _('Your vote for {} has been recorded as {}').format(poll, vote)
        else:
            msg = _("The correct format is /bot vote <vote> - <poll>")
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        simple = _('An Error Occurred')
        msg = _("{} -- {}").format(str(e), event.text)
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)

def results(bot, event, *args):
    '''Get's results of poll. Format is /bot results <poll>'''
    try:
        poll = ' '.join(args)
        votes = []
        names = []
        msg = []
        winners = []
        path = bot.memory.get_by_path(["polls", poll])
        for person in path:
            names.append(person)
            vote = path[person]
            votes.append(vote)
        for i in range(len(names)):
            result = '{} voted {}<br>'.format(names[i], votes[i])
            msg.append(result)
        count = Counter(votes)
        freqlist = list(count.values())
        maxcount = max(freqlist)
        total = freqlist.count(maxcount)
        common = count.most_common(total)
        for item in common:
            winners.append(str(item[0]))
        freq = str(common[0][1])
        if len(winners) == 1:
            msg.append('<br>THE WINNER IS <b>{}</b> with <b>{}</b> votes'.format(winners[0], freq))
        else:
            msg.append('<br>THE WINNERS ARE <b>{}</b> with <b>{}</b> votes'.format(', '.join(winners), freq))
        final = ''.join(msg)
        yield from bot.coro_send_message(event.conv, final)
    except BaseException as e:
        simple = _('Either an error occurred or there is no poll by that name')
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)
