from app.services.check_services import *
from app.services.weather_service import *
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

@pytest.mark.asyncio
async def test_should_return_false_if_date_not_in_range(patch_datetime_now):
    data = { "@date": { "after": "2024-01-18", "before": "2024-03-15" } }
    arguments = {}
    assert await check_service.run(data, arguments) == False

@pytest.mark.asyncio
async def test_should_return_true_if_date_in_range(patch_datetime_now):
    print(datetime.datetime.now())
    data = { "@date": { "after": "2024-01-18", "before": "2024-03-23" } }
    arguments = {}
    assert await check_service.run(data, arguments) == True

@pytest.mark.asyncio
async def test_should_return_false_if_not_eq_level():
    data = { "@level": { "eq": 40 } }
    arguments = { "level": 25 }
    assert await check_service.run(data, arguments) == False

@pytest.mark.asyncio
async def test_should_return_true_if_eq_level():
    data = { "@level": { "eq": 25 } }
    arguments = { "level": 25 }
    assert await check_service.run(data, arguments) == True

@pytest.mark.asyncio
async def test_should_return_false_if_not_lt_level():
    data = { "@level": { "lt": 40 } }
    arguments = { "level": 50 }
    assert await check_service.run(data, arguments) == False

@pytest.mark.asyncio
async def test_should_return_true_if_lt_level():
    data = { "@level": { "lt": 40 } }
    arguments = { "level": 30 }
    assert await check_service.run(data, arguments) == True

@pytest.mark.asyncio
async def test_should_return_false_if_not_gt_lt_level():
    data = { "@level": { "gt": 20, "lt": 40 } }
    arguments = { "level": 50 }
    assert await check_service.run(data, arguments) == False

@pytest.mark.asyncio
async def test_should_return_true_if_gt_lt_level():
    data = { "@level": { "gt": 20, "lt": 40 } }
    arguments = { "level": 30 }
    assert await check_service.run(data, arguments) == True

@pytest.mark.asyncio
@mock.patch.object(WeatherService, 'get_weather')
async def test_should_return_false_if_meteo_not_gt(mockget):
    mockget.return_value = 10
    data = { "@meteo": { "is": "clear", "temp": { "gt": "15" } } }
    arguments = {"meteo": { "town": "Chambon" }}
    assert await check_service.run(data, arguments) == False

@pytest.mark.asyncio
@mock.patch.object(WeatherService, 'get_weather')
async def test_should_return_true_if_meteo_gt(mockget):
    mockget.return_value = 20
    data = { "@meteo": { "is": "clear", "temp": { "gt": "15" } } }
    arguments = {"meteo": { "town": "Chambon" }}
    assert await check_service.run(data, arguments) == True

@pytest.mark.asyncio
@mock.patch.object(WeatherService, 'get_weather')
async def test_should_return_false_if_meteo_not_in_range(mockget):
    mockget.return_value = 40
    data = { "@meteo": { "is": "clear", "temp": { "gt": "15", "lt": "30" } } }
    arguments = {"meteo": { "town": "Chambon" }}
    assert await check_service.run(data, arguments) == False
    mockget.assert_called_once_with("Chambon") 

@pytest.mark.asyncio
@mock.patch.object(WeatherService, 'get_weather')
async def test_should_return_true_if_meteo_in_range(mockget):
    mockget.return_value = 25
    data = { "@meteo": { "is": "clear", "temp": { "gt": "15", "lt": "30" } } }
    arguments = {"meteo": { "town": "Chambon" }}
    assert await check_service.run(data, arguments) == True
    mockget.assert_called_once_with('Chambon')