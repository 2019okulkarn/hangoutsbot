import io
import plugins
from apikeys import cx, gapi, image
from links import shorten
from control import *
import json
from requests import get
import traceback
from urllib.parse import quote
import aiohttp
import os

def _initialise():
    plugins.register_user_command(['lmgtfy', 'google', 'g'])

def search(term):
    r = get('https://www.googleapis.com/customsearch/v1', params={'key': gapi, 'cx': cx, 'q': term})
    data = json.loads(r.text)
    if 'items' not in data:
        return "Google couldn't find anything"
    else:
        title = data['items'][0]['title']
        link = data['items'][0]['link']
        return {
            'title': title,
            'link': link
        }

def imagesearch(term):
    r = get('https://www.googleapis.com/customsearch/v1', params={'key': gapi, 'cx': image, 'q': term, 'defaultToImageSearch': 'True'})
    data = json.loads(r.text)
    if 'items' not in data:
        return 'No Images Found'
    else:
        link = data['items'][0]['pagemap']['cse_image'][0]['src']
        return link

def google(bot, event, *args):
    try:
        if args:
            if not args[0] == '-i':
                s = search(str(' '.join(args)))
                if s == "Google couldn't find anything":
                    msg = _(s)
                else:
                    msg = _('Google says:<br>**{}**<br>{}').format(s['title'], s['link'])
                yield from bot.coro_send_message(event.conv, msg)
            else:
                term = ' '.join(args[1:])
                s = imagesearch(term)
                if s == "No Images Found":
                    msg = _(s)
                    yield from bot.coro_send_message(event.conv, msg)
                else:
                    link_image = s
                    filename = os.path.basename(link_image)
                    r = yield from aiohttp.request('get', link_image)
                    raw = yield from r.read()
                    image_data = io.BytesIO(raw)

                    image_id = yield from bot._client.upload_image(image_data, filename=filename)

                    yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)               
        else:
            msg = _('What should I ask Google to answer?')
            yield from bot.coro_send_message(event.conv, msg)
    except:
        tb = traceback.format_exc()
        msg = _('{} -- {}').format(tb, event.text)
        yield from bot.coro_send_message(CONTROL, msg)
        yield from bot.coro_send_message(event.conv, _('An Error Occured'))


def g(bot, event, *args):
    try:
        if args:
            if not args[0] == '-i':
                s = search(str(' '.join(args)))
                if s == "Google couldn't find anything":
                    msg = _(s)
                else:
                    msg = _('Google says:<br>**{}**<br>{}').format(s['title'], s['link'])
                yield from bot.coro_send_message(event.conv, msg)
            else:
                term = ' '.join(args[1:])
                s = imagesearch(term)
                if s == "No Images Found":
                    msg = _(s)
                    yield from bot.coro_send_message(event.conv, msg)
                else:
                    link_image = s
                    filename = os.path.basename(link_image)
                    r = yield from aiohttp.request('get', link_image)
                    raw = yield from r.read()
                    image_data = io.BytesIO(raw)

                    image_id = yield from bot._client.upload_image(image_data, filename=filename)

                    yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)               
        else:
            msg = _('What should I ask Google to answer?')
            yield from bot.coro_send_message(event.conv, msg)
    except:
        tb = traceback.format_exc()
        msg = _('{} -- {}').format(tb, event.text)
        yield from bot.coro_send_message(CONTROL, msg)
        yield from bot.coro_send_message(event.conv, _('An Error Occured'))
def lmgtfy(bot, event, *args):
    '''Returns an lmgtfy link from http://lmgtfy.com/ Format is /bot lmgtfy <what to google>'''
    try:
        if args:
            query = ' '.join(args)
            search = quote(query)
            url = 'http://lmgtfy.com/?q=' + search
            msg = _('{}').format(shorten(url))
        else:
            msg = _('{}').format(shorten('http://lmgtfy.com/?q=urbandictionary%20dolphin'))
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROL, msg)
