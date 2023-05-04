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

lat, lon = 42.816095253156846, -118.52502832775187
api_url = f"https://history.openweathermap.org/data/2.5/aggregated/year?lat={lat}&lon={lon}&appid={appid}"
res = requests.get(api_url)
print(res)
res = res["result"]
spring_entry = res[100]
mean_temp = spring_entry["temp"]["mean"]
mean_humidity = spring_entry["humidity"]["mean"]
mean_wind = spring_entry["wind"]["mean"]
mean_precipitation = spring_entry["precipitation"]["mean"]
print("NO WILDFIRE: SPRING")
print(f"  mean temperature: {mean_temp}")
print(f"  mean humidity: {mean_humidity}")
print(f"  mean wind: {mean_wind}")
print(f"  mean precipitation: {mean_precipitation}")
summer_entry = res[180]
mean_temp = summer_entry["temp"]["mean"]
mean_humidity = summer_entry["humidity"]["mean"]
mean_wind = summer_entry["wind"]["mean"]
mean_precipitation = summer_entry["precipitation"]["mean"]
print("NO WILDFIRE: SUMMER")
print(f"  mean temperature: {mean_temp}")
print(f"  mean humidity: {mean_humidity}")
print(f"  mean wind: {mean_wind}")
print(f"  mean precipitation: {mean_precipitation}")

lat, lon = 44.66581129340926, -122.60229630435458
api_url = f"https://history.openweathermap.org/data/2.5/aggregated/year?lat={lat}&lon={lon}&appid={appid}"
response = requests.get(api_url)
spring_entry = res[100]
mean_temp = spring_entry["temp"]["mean"]
mean_humidity = spring_entry["humidity"]["mean"]
mean_wind = spring_entry["wind"]["mean"]
mean_precipitation = spring_entry["precipitation"]["mean"]
print("WILDFIRE: SPRING")
print(f"  mean temperature: {mean_temp}")
print(f"  mean humidity: {mean_humidity}")
print(f"  mean wind: {mean_wind}")
print(f"  mean precipitation: {mean_precipitation}")
summer_entry = res[180]
mean_temp = summer_entry["temp"]["mean"]
mean_humidity = summer_entry["humidity"]["mean"]
mean_wind = summer_entry["wind"]["mean"]
mean_precipitation = summer_entry["precipitation"]["mean"]
print("WILDFIRE: SUMMER")
print(f"  mean temperature: {mean_temp}")
print(f"  mean humidity: {mean_humidity}")
print(f"  mean wind: {mean_wind}")
print(f"  mean precipitation: {mean_precipitation}")


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