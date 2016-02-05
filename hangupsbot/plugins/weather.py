import pywapi
import plugins
import string
import links
from control import *
def _initialise():
    plugins.register_user_command(['weather', 'forecast'])

def weather(bot, event, *args): 
    '''Gets weather from weather.com. Defaults to Chantilly, VA if no location given. Format is /bot weather <city>,<state/country>'''
    try:
        if args:
            place = ' '.join(args)
            lookup = pywapi.get_location_ids(place)
            for i in lookup:
                location_id = i
        else:
            location_id= 'USVA0140'
            yield from bot.coro_send_message(event.conv, _("No location given; defaulting to Chantilly, VA"))
        weather_com_result = pywapi.get_weather_from_weather_com(location_id , units = 'imperial' )
        condition = weather_com_result['current_conditions']['text'].lower()
        temp = weather_com_result['current_conditions']['temperature']
        feelslike = weather_com_result['current_conditions']['feels_like']
        place = weather_com_result['location']['name']
        url = links.shorten('http://www.weather.com/weather/today/l/' + location_id)
        msg = _('<b>Today in {}:</b><br>Temp: {}°F (Feels like: {}°F)<br>Conditions: {}<br>For more information visit {}').format(place, temp, feelslike, condition, url)
        yield from bot.coro_send_message(event.conv, msg)
    except BaseException as e:
        msg = _('{} -- {}').format(str(e), event.text)
        yield from bot.coro_send_message(CONTROL, msg)

def forecast(bot, event, *args):
    if args:
        place = ' '.join(args)
        lookup = pywapi.get_location_ids(place)
        for i in lookup:
            location_id = i
    else:
        location_id= 'USVA0140'
        yield from bot.coro_send_message(event.conv, _("No location given; defaulting to Chantilly, VA"))
    weather_com_result = pywapi.get_weather_from_weather_com(location_id , units = 'imperial' )
    place = weather_com_result['location']['name']
    high = weather_com_result['forecasts'][0]['high']
    low = weather_com_result['forecasts'][0]['low']
    day = weather_com_result['forecasts'][0]['day']['text']
    if day == '':
        day = 'N/A'
    night = weather_com_result['forecasts'][0]['night']['text']
    if night == '':
        night = 'N/A'
    date = weather_com_result['forecasts'][0]['date']
    url = links.shorten('http://www.weather.com/weather/today/l/' + location_id)
    msg=_("<b>Forecast for {} on {}:</b><br>Conditions: Day - {}; Night - {}<br>High: {}<br>Low: {}<br>For more information visit {}").format(place, date, day, night, high, low, url)
    yield from bot.coro_send_message(event.conv, msg)
