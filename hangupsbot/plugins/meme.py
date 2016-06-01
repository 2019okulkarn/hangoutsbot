from imgurpython import ImgurClient
import plugins
from apikeys import imgur_client, imgur_secret
import random
import logging
import aiohttp
from control import *
import os
import io

logger = logging.getLogger(__name__)

def _initialize():
    plugins.register_user_command(["meme"])

def meme(bot, event, *args):
    #try:
        client = ImgurClient(imgur_client, imgur_secret)
        funny = client.subreddit_gallery('funny')
        link_image = random.choice(funny).link
        logger.info("getting {}".format(link_image))
        filename = os.path.basename(link_image)
        r = yield from aiohttp.request('get', link_image)
        raw = yield from r.read()
        image_data = io.BytesIO(raw)
        image_id = yield from bot._client.upload_image(image_data, filename=filename)
        yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)
    #except Exception e:
        #msg = _('{} -- {}').format(str(e), event.text)
        #yield from bot.coro_send_message(CONTROL, msg)
