from app.services.check_services import *
from app.services.weather_service import *
from app.services.restrictions_services import *
from unittest import mock
import pytest

FAKE_TIME = datetime.datetime(2024, 3, 22)

@pytest.fixture
def patch_datetime_now(monkeypatch):
    class mydatetime(datetime.datetime):
        @classmethod
        def now(cls):
            return FAKE_TIME
    
    monkeypatch.setattr(datetime, 'datetime', mydatetime)

weather_service = WeatherService(None, None)
check_service = CheckService(weather_service)
restriction_service = RestrictionsService(check_service)

@pytest.mark.asyncio
@mock.patch.object(WeatherService, 'get_weather')
async def test_should_return_true_if_tree_is_good(mockget, patch_datetime_now):
    mockget.return_value = 25
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@or": [ { "@level": { "eq": 40 } }, { "@and": [ { "@level": { "lt": 30, "gt": 15 } }, { "@meteo": { "is": "clear", "temp": { "gt": "15" } } } ] } ] } ]
    arguments = { "level": 25, "meteo": { "town": "Chambon" } }
    assert await restriction_service.run(data, arguments) == True

@pytest.mark.asyncio
@mock.patch.object(WeatherService, 'get_weather')
async def test_should_return_false_if_tree_not_good(mockget, patch_datetime_now):
    mockget.return_value = 0
    data = [ { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }, { "@or": [ { "@level": { "eq": 40 } }, { "@and": [ { "@level": { "lt": 30, "gt": 15 } }, { "@meteo": { "is": "clear", "temp": { "gt": "15" } } } ] } ] } ]
    arguments = { "level": 25, "meteo": { "town": "Chambon" } }
    assert await restriction_service.run(data, arguments) == False