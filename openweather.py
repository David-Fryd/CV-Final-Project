# open weather: can query yearly aggregation, monthly aggregation, or daily aggregation given latitude / longitude
# gives you temperature, pressure, humidity, temp_min, temp_max, wind, clouds, weather
# seems like it costs $0.12 / API call?

# alternative: pyowm library
#   PyOWM is a client Python wrapper library for OpenWeatherMap web APIs. It allows quick and easy consumption of OWM
#   data from Python applications via a simple object model and in a human-friendly fashion.

import pyowm
import requests

appid = "1cdbd781930c57b4b5d45de51264967c" # api key
owm = pyowm.OWM(appid)

def OPENWEATHER_get_weather(coordinates):
    weather = dict()
    for coordinate in coordinates:
        lat, lon = coordinate['x'], coordinate['y']
        start, end = 1640995200, 1672444800 # january 1 2022 - december 31 2022
        api_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start}&end={end}&appid={appid}"
        response = requests.get(api_url)
        weather[(lat, lon)] = {
            "temperature": response["list"]["main"]["temp"],
            "humidity": response["list"]["main"]["humidity"],
            "wind speed": response["list"]["wind"]["speed"],
            "rain 3h": response["list"]["rain"]["3h"],
        }
    return weather

def PYOWM_get_weather(coordinates):
    weather = dict()
    for coordinate in coordinates:
        lat, lon = coordinate['x'], coordinate['y']
        start, end = 1640995200, 1672444800 # january 1 2022 - december 31 2022
        history = owm.weather_history_at_place(place, start, end) # didn't look like there was a way to query weather history based on latitude longitude, so we may have to stick with api calls
        day = history.get_weathers()[0]
        weather[(lat, lon)] = {
            "temperature": day.get_temperature('celsius'),
            "humidity": day.get_humidity(),
            "wind speed": day.get_wind()["speed"],
            "rain 3h": day.get_rain()["3h"],
        }