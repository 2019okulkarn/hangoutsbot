from espn import *
import plugins
from control import *

def _initialise():
    plugins.register_user_command(['score'])

def score(bot, event, *args):
    '''Get's scores from ESPN. Format is /bot score <league abbrev (nfl, nba, mlb, nhl, ncf[college])> - <team city (eg. Denver)> <i>Example: /bot score nfl - denver</i>'''
    try:
        list_ = ' '.join(args).split(' - ')
        sport = list_[0]
        team = list_[1]
        scores = get_scores(sport.lower(), team.lower())
        first = str(scores).split(':')
        id = str(first[0])
        id = id[2:-1]
        scoreslist = scores[id]
        team1 = scoreslist[0]
        team1score = scoreslist[1]
        team2 = scoreslist[2]
        team2score = scoreslist[3]
        time = scoreslist[4]
        msg = _('<b>{}:</b> {}<br><b>{}:</b> {}<br>{} - MAY NOT BE ACCURATE DURING GAMES').format(team1, team1score, team2, team2score, time)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        simple = _('Unable to find scores')
        msg = _(str(e))
        yield from bot.coro_send_message(event.conv, simple)
        yield from bot.coro_send_message(CONTROL, msg)
	
	    

