import requests
import json

class GeocodingApi:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        #https://openweathermap.org/api/geocoding-api
        self.base_url = "http://api.openweathermap.org/geo/1.0/"
        self.session = requests.Session()

    """
    [{'name': 'London', 'local_names': {'vo': 'London', 'fo': 'London'}, 
    'lat': 51.5073219, 'lon': -0.1276474, 'country': 'GB', 'state': 'England'}]
    """
    async def get_geocoding(self, town):
        response = self.session.get(self.base_url + f"direct?q={town}&limit=5&appid={self.api_key}")
        try:
            return json.loads(response.text)[0]
        except Exception:
            raise Exception(f"Failed fetching geocoding : {response.text}")
        
class WeatherApi:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        #https://openweathermap.org/current
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.session = requests.Session()

    """
    {'coord': {'lon': -0.1278, 'lat': 51.5074}, 
    'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 
    'base': 'stations', 'main': {'temp': 284.51, 'feels_like': 283.45, 'temp_min': 283.02, 
    'temp_max': 286.05, 'pressure': 999, 'humidity': 67}, 'visibility': 10000, 
    'wind': {'speed': 4.47, 'deg': 91, 'gust': 5.81}, 
    'clouds': {'all': 100}, 'dt': 1711370357, 
    'sys': {'type': 2, 'id': 2075535, 'country': 'GB', 'sunrise': 1711345858, 'sunset': 1711390898}, 
    'timezone': 0, 'id': 2643743, 'name': 'London', 'cod': 200}
    """
    async def get_current_weather(self, lat, lon):
        response = self.session.get(self.base_url + f"weather?lat={lat}&lon={lon}&appid={self.api_key}")
        try:
            data = json.loads(response.text)
            return data["main"]["temp"]
        except Exception:
            raise Exception(f"Failed fetching weather : {response.text}")

class WeatherService:
    def __init__(self, geocoding_api: GeocodingApi, weather_api: WeatherApi) -> None:
        self._geocoding_api = geocoding_api
        self._weather_api = weather_api

    async def get_weather(self, town):
        response = await self._geocoding_api.get_geocoding(town)
        return await self._weather_api.get_current_weather(response["lat"], response["lon"])