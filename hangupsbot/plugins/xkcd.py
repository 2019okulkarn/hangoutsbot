import aiohttp, asyncio, io, logging, os, re

import plugins

from control import *

from links import *

from random import choice as choose

import pykcd

logger = logging.getLogger(__name__)


def _initialise():
    plugins.register_user_command(["xkcd"])
    plugins.register_handler(_thirty_seven, type="message")

@asyncio.coroutine
def _thirty_seven(bot, event, command):
    if '-ass ' in str(event.text):
        link_image = str(pykcd.XKCDStrip(37).image_link)
        filename = os.path.basename(link_image)
        r = yield from aiohttp.request('get', link_image)
        raw = yield from r.read()
        image_data = io.BytesIO(raw)
        link = shorten(link_image)
        image_id = yield from bot._client.upload_image(image_data, filename=filename)
        yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)
        yield from bot.coro_send_message(event.conv, _('{}').format(link))



def xkcd(bot, event, *args):
    '''Gets xkcd comic. Random number is chosen if number is not given. Format is /bot xkcd <number>'''
    try:
        numlist =  list(range(1, 1631))
        if len(args) == 1 and args[0].isdigit():
            num = int(args[0])
            link_image = str(pykcd.XKCDStrip(num).image_link)
            title = str(pykcd.XKCDStrip(num).title)
            alt_text = str(pykcd.XKCDStrip(num).alt_text)
            link = 'http://xkcd.com/' + str(num)
        else:
            chosencomic = choose(numlist)
            num = int(chosencomic)
            link_image = str(pykcd.XKCDStrip(num).image_link)
            title = str(pykcd.XKCDStrip(num).title)
            alt_text = str(pykcd.XKCDStrip(num).alt_text)
            link = 'http://xkcd.com/' + str(num)

        logger.info("getting {}".format(link_image))
        filename = os.path.basename(link_image)
        r = yield from aiohttp.request('get', link_image)
        raw = yield from r.read()
        image_data = io.BytesIO(raw)
        msg = _('Title: {}<br>Caption: {}<br>Number: {}<br>Link: {}').format(title, alt_text, num, link)
        image_id = yield from bot._client.upload_image(image_data, filename=filename)
        yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROL,msg)
