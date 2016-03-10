from requests import get
import json
import plugins
from apikeys import wordnik


def _initialise():
    plugins.register_user_command(["define"])


def defineword(word):
    try:
        payload = {'limit': '1', 'includeRelated': 'true',
                   'sourceDictionaries': 'all', 'api_key': wordnik}
        url = 'http://api.wordnik.com:80/v4/word.json/{}/definitions'.format(
            str(word))
        r = get(url, params=payload)
        data = json.loads(r.text)
        wordused = data[0]["word"]
        definition = data[0]["text"]
        return "<b>Word: {}</b>\nDefinition: {}".format(wordused, definition)
    except:
        return "No Definition for {} found".format(str(word))


def define(bot, event, *args):
    if len(args) == 1:
        word = args[0]
        definition = defineword(word)
        msg = _(definition)
    else:
        msg = _("I can only define one word at a time.")
    yield from bot.coro_send_message(event.conv, msg)
