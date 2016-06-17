from apikeys import google_server_key
from requests import get
from datetime import datetime
from pytz import timezone
from time import time
import plugins

def timeat(place):
    payload = {"key": google_server_key, "address": place}
    r = get("https://maps.googleapis.com/maps/api/geocode/json", params=payload)
    data = r.json()
    latitude =  data["results"][0]["geometry"]["location"]["lat"]
    longitude =  data["results"][0]["geometry"]["location"]["lng"]
    payload2 = {"key": google_server_key, "location": "{},{}".format(latitude, longitude), "timestamp": time() }
    req = get("https://maps.googleapis.com/maps/api/timezone/json", params=payload2)
    data2 = req.json()
    tz = data2["timeZoneId"]
    current_time = datetime.now(timezone(tz)).ctime()
    return {"location": data["results"][0]["formatted_address"], "time": current_time}

def _initialize():
    plugins.register_user_command(["timein"])

def timein(bot, event, *args):
    try:
        if args:
            returned = timeat(' '.join(args))
            msg = _("<strong>Time in {}:</strong>\n{}").format(returned["location"], returned["time"])
        else:
            msg = "Where do you want the time for?"
        yield from bot.coro_send_message(event.conv, msg)
    except Exception as e:
        yield from bot.coro_send_message(CONTROL, str(e))
        yield from bot.coro_send_message(event.conv, "An Error Occurred")
