from requests import get
import plugins
from apikeys import mashape
from control import *
from links import shorten
from urllib.parse import quote as sanitize
import json

def getlyrics(title, artist):
    response = get("https://musixmatchcom-musixmatch.p.mashape.com/wsr/1.1/track.search?f_has_lyrics=1&page=1&page_size=1&q_track=" + sanitize(title) + "&q_artist=" + sanitize(artist),
    headers={
        "X-Mashape-Key": mashape,
        "Accept": "application/json"
            }
        )
    data = json.loads(response.text)
    name = data[0]["track_name"]
    artst = data[0]["artist_name"]
    trackid = data[0]["track_id"]
    lyrget = get("https://musixmatchcom-musixmatch.p.mashape.com/wsr/1.1/track.lyrics.get?track_id=" + str(trackid), headers={
        "X-Mashape-Key": mashape,
        "Accept": "application/json"
            }
            )
    data2 = json.loads(lyrget.text)
    lyrics = data2["lyrics_body"]
    url = 'https://www.musixmatch.com/lyrics/' + artist.replace(" ", "-") + '/' + title.replace(" ", "-")
    return {
    'name': name,
    'artist': artst,
    'lyrics': lyrics,
    'url': url
    }

def _initialise():
	plugins.register_user_command(['lyrics'])

def lyrics(bot, event, *args):
	try:
		message = ' '.join(args)
		title = message.split(' by ')[0]
		artist = message.split(' by ')[1]
		g = getlyrics(title, artist)
		msg = _('<b>{} by {}</b><br>{}<br>Full Lyrics: {}').format(g['name'], g['artist'], g['lyrics'], shorten(g['url']))
		yield from bot.coro_send_message(event.conv, msg)
	except BaseException as e:
		simple = _('The correct format is /bot lyrics <title> by <artist>')
		msg = _('{} -- {}').format(str(e), event.text)
		yield from bot.coro_send_message(event.conv, simple)
		yield from bot.coro_send_message(CONTROL, msg)
