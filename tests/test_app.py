from starlette.testclient import TestClient
from unittest.mock import  ANY, AsyncMock, patch
from app.database.models.operation import *
from main import app

client = TestClient(app)

@patch('app.routers.operations.get_db_service')
def test_get_operation(mock_get_db):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db
    name = "ChangeGearbox"
    priority = 1
    restrictions = [
      {
        "@date": {
          "after": "2024-01-18",
          "before": "2024-03-15"
        }
      }]
    mock_db.get_operation.return_value = {
    "name": name,
    "priority": priority,
    "restrictions": restrictions
    }
    
    response = client.get(f'/get_operation/?name={name}')
    assert response.status_code == 200
    operation = response.json()["result"]
    assert operation["name"] == name
    assert operation["priority"] == priority
    assert operation["restrictions"] == restrictions
    mock_db.get_operation.assert_called_once_with(name)

@patch('app.routers.operations.get_db_service')
def test_save_operation(mock_get_db):
    mock_db = AsyncMock()
    mock_get_db.return_value = mock_db
    name = "ChangeGearbox"
    priority = 1
    restrictions = [
            {
            "@date": {
                "after": "2024-01-18",
                "before": "2024-03-15"
            }
            },
            {
            "@or": [
                {
                "@level": {
                    "eq": 40
                }
                },
                {
                "@and": [
                    {
                    "@level": {
                        "lt": 30,
                        "gt": 15
                    }
                    },
                    {
                    "@meteo": {
                        "is": "clear",
                        "temp": {
                        "gt": "15"
                        }
                    }
                    }
                ]
                }
            ]
            }
        ]
    data = {
        "_id": "...",
        "name": name,
        "priority": { "value": priority },
        "restrictions": restrictions
        }
    id = 1
    mock_db.save_operation.return_value = id
    
    response = client.post(f'/save_operation/', json=data)
    assert response.status_code == 200
    assert response.json() == {"Status": "Success", "id": id}
    mock_db.save_operation.assert_called_once_with(name, priority, restrictions)

@patch('app.routers.operations.get_db_service')
@patch('app.routers.operations.get_restriction_service')
def test_validate_operation_success(mock_get_db, mock_get_restriction_service):
    mock_db = AsyncMock()

    mock_get_db.return_value = mock_db
    operation_name = "ChangeGearbox"
    priority = 3
    mock_db.get_operation.return_value = Operation(operation_name, priority,  [
      {
        "@date": {
          "after": "2024-01-18",
          "before": "2024-03-15"
        }
      }]) 

    mock_get_restriction_service.return_value = mock_db
    mock_db.run.return_value = True

    data = {
                "operation_name": "ChangeGearbox",
                "arguments": {
                    "level": 25,
                    "meteo": { "town": "Chambon" }
                }
    }
    response = client.post(f'/validate_operation/', json=data)
    assert response.status_code == 200
    assert response.json() == {
                    "operation_name": operation_name,
                    "status": "accepted",
                    "priority": { "value": priority }
                    }
    
@patch('app.routers.operations.get_db_service')
@patch('app.routers.operations.get_restriction_service')
def test_validate_operation_failure(mock_get_db, mock_get_restriction_service):
    mock_db = AsyncMock()

    mock_get_db.return_value = mock_db
    operation_name = "ChangeGearbox"
    priority = 3
    mock_db.get_operation.return_value = Operation(operation_name, priority,  [
      {
        "@date": {
          "after": "2024-01-18",
          "before": "2024-03-15"
        }
      }]) 

    mock_get_restriction_service.return_value = mock_db
    mock_db.run.return_value = False

    data = {
                "operation_name": "ChangeGearbox",
                "arguments": {
                    "level": 25,
                    "meteo": { "town": "Chambon" }
                }
    }
    response = client.post(f'/validate_operation/', json=data)
    assert response.status_code == 200
    assert response.json() == {
            "operation_name": operation_name,
            "status": "denied",
            "reasons": {
                }
            }
