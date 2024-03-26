from app.services.weather_service import *
from unittest import mock
import requests
import json
import pytest

@pytest.mark.asyncio
@mock.patch.object(requests.Session, 'get')
async def test_fetch_geocoding_api(mockget):
    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    lat = 51.5156177
    lon = -0.0919983
    api_key = "test"
    mockresponse.text = json.dumps([{'name': 'London', 'local_names': {'vo': 'London', 'fo': 'London'}, 
    'lat': lat, 'lon': lon, 'country': 'GB', 'state': 'England'}])

    api = GeocodingApi(api_key)
    response = await api.get_geocoding("London")
    mockget.assert_called_once_with(f'http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={api_key}')
    assert response["lat"] == lat
    assert response["lon"] == lon

@pytest.mark.asyncio
@mock.patch.object(requests.Session, 'get')
async def test_fetch_weather_api(mockget):
    mockresponse = mock.Mock()
    mockget.return_value = mockresponse
    temp = 292.55
    lat = 51.5156177
    lon = -0.0919983
    api_key = "test"
    mockresponse.text = json.dumps( {'coord': {'lon': lon, 'lat': lat}, 
    'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04d'}], 
    'base': 'stations', 'main': {'temp': temp, 'feels_like': 283.45, 'temp_min': 283.02, 
    'temp_max': 286.05, 'pressure': 999, 'humidity': 67}, 'visibility': 10000, 
    'wind': {'speed': 4.47, 'deg': 91, 'gust': 5.81}, 
    'clouds': {'all': 100}, 'dt': 1711370357, 
    'sys': {'type': 2, 'id': 2075535, 'country': 'GB', 'sunrise': 1711345858, 'sunset': 1711390898}, 
    'timezone': 0, 'id': 2643743, 'name': 'London', 'cod': 200})

    api = WeatherApi(api_key)
    response = await api.get_current_weather(lat, lon)
    mockget.assert_called_once_with(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}')
    assert response == temp