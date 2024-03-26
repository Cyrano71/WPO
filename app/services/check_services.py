from app.services.weather_service import WeatherService
from enum import Enum
import datetime

class RANGE_VALUE_OPERATIONS(Enum):
        EQUAL = "eq"
        LESS_THAN = "lt"
        GREATER_THAN = "gt"

class CHECKS(Enum):
    Date = "date"
    Meteo = "meteo"
    Level = "level"

class CheckService:
    def __init__(self, weather_service: WeatherService) -> None:
        self._weather_service = weather_service
        self.checks = {
        CHECKS.Date: lambda a, _ : self.check_range_date(a[f"@{CHECKS.Date.value}"]),
        CHECKS.Meteo: lambda a, b : self.check_meteo(a[f"@{CHECKS.Meteo.value}"], b[CHECKS.Meteo.value]),
        CHECKS.Level: lambda a, b : self.check_range_value(a[f"@{CHECKS.Level.value}"], b[CHECKS.Level.value]),
    }
        
    async def run(self, item, arguments):
        for check in self.checks:
            if f"@{check.value}" in item:
                return await self.checks[check](item, arguments)
            
        raise Exception(f"unknwon item : {item}")

    async def check_range_date(self, range):
        now = datetime.datetime.now()
        after = datetime.datetime.strptime(range['after'], '%Y-%m-%d')
        before  = datetime.datetime.strptime(range['before'], '%Y-%m-%d')
        return now <= before and now >= after
    
    async def check_meteo(self, conditions, town):
        value = await self._weather_service.get_weather(town["town"])
        required = conditions["temp"]
        return await self.check_range_value(required, value)
    
    async def check_range_value(self, required, value):
        if RANGE_VALUE_OPERATIONS.EQUAL.value in required:
            return value == float(required[RANGE_VALUE_OPERATIONS.EQUAL.value])
        result = True
        if RANGE_VALUE_OPERATIONS.LESS_THAN.value in required:
            result &= value < float(required[RANGE_VALUE_OPERATIONS.LESS_THAN.value])
        if RANGE_VALUE_OPERATIONS.GREATER_THAN.value in required:
            result &= value > float(required[RANGE_VALUE_OPERATIONS.GREATER_THAN.value])
        return result