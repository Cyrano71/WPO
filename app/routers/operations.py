from fastapi import APIRouter, HTTPException, status
from app.services.weather_service import *
from app.services.check_services import *
from app.services.restrictions_services import *
from app.services.database_service import *
from app.schemas.operations_requests import *

router = APIRouter()

weather_service = None
db_service = None
restriction_service = None

async def build(config):
    global weather_service
    weather_service = WeatherService(GeocodingApi(config.get("API", "key")), WeatherApi(config.get("API", "key")))
    check_service = CheckService(weather_service)
    global restriction_service
    restriction_service = RestrictionsService(check_service)
    global db_service
    db_service = DatabaseService()
    
async def get_weather_service():
    return weather_service

async def get_db_service():
    return db_service

async def get_restriction_service():
    return restriction_service

@router.post("/validate_operation/")
async def validate_operation(data: PriorityDataGetRequest):
    db_service = await get_db_service()
    operation = await db_service.get_operation(data.operation_name)
    restriction_service = await get_restriction_service()
    validation = await restriction_service.run(operation.restrictions, data.arguments.model_dump())
    if validation:
        return {
                    "operation_name": data.operation_name,
                    "status": "accepted",
                    "priority": { "value": operation.priority }
                    }
    return {
            "operation_name": data.operation_name,
            "status": "denied",
            "reasons": {
                }
            }

@router.get("/get_weather/")
async def get_weather(name: str):
    service = await get_weather_service()
    result = await service.get_weather(name)
    return {"result": result}

@router.get("/get_operation/")
async def get_operation(name: str):
    service = await get_db_service()
    result = await service.get_operation(name)
    return {"result": result}

@router.post("/save_operation/")
async def save_operation(item: OperationDataRequest):
    try:
        service = await get_db_service()
        id = await service.save_operation(item.name, item.priority.value, item.restrictions)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    
    return {"Status": "Success", "id": id}