# open weather: can query yearly aggregation, monthly aggregation, or daily aggregation given latitude / longitude
# gives you temperature, pressure, humidity, temp_min, temp_max, wind, clouds, weather
# seems like it costs $0.12 / API call?

# alternative: pyowm library
#   PyOWM is a client Python wrapper library for OpenWeatherMap web APIs. It allows quick and easy consumption of OWM
#   data from Python applications via a simple object model and in a human-friendly fashion.

import pyowm
import requests

appid = "abc" # api key
owm = pyowm.OWM(appid)

def OPENWEATHER_get_weather(coordinate):
    lat, lon = coordinate['x'], coordinate['y']
    api_url = f"https://history.openweathermap.org/data/2.5/aggregated/year?lat={lat}&lon={lon}&appid={appid}"
    res = requests.get(api_url)["result"]
    yearly_aggregate = dict()
    for entry in res:
        month = entry["month"]
        day = entry["day"]
        mean_temp = entry["temp"]["mean"]
        mean_humidity = entry["humidity"]["mean"]
        mean_wind = entry["wind"]["mean"]
        mean_precipitation = entry["precipitation"]["mean"]
        if month not in yearly_aggregate:
            yearly_aggregate[month] = dict()
        yearly_aggregate[month][day] = {
            "temp": mean_temp,
            "humidity": mean_humidity,
            "wind_speed": mean_wind,
            "precipitation": mean_precipitation
        }

def collect_weather_stats(coordinates):
    weather_stats = dict()
    for coordinate in coordinates:
        yearly_aggregate = OPENWEATHER_get_weather(coordinate)
        weather_stats[coordinate] = yearly_aggregate
    return weather_stats