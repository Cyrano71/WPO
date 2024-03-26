# Test WPO 

## Installation method

1. Set up EC2 instance Amazon Linux 2023 AMI

```shell
sudo yum install git -y
git clone https://github.com/Cyrano71/WPO.git
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
 ```

2. Install the required packages

   ```
   cd WPO
   pip install -r requirements.txt
   ```

3. Add in the **config.ini** your api key

3. Start the app

   ```shell
   python3 main.py
   ```

4. Check the app on [notes](http://localhost:8000/docs)
Open your browser and navigate to [docs](http://localhost:8000/docs) to view the swagger documentation for the api.

add operation with validation failure
```
{
  "_id": "...",
  "name": "ChangeGearbox",
  "priority": { "value": 1 },
  "restrictions": [
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
}

{
  "operation_name": "ChangeGearbox",
  "arguments": {
    "level": 25,
    "meteo": { "town": "Chambon" }
}
}
```

add operation with validation success
```
{
  "_id": "...",
  "name": "ChangeGearbox",
  "priority": { "value": 1 },
  "restrictions": [
    {
      "@date": {
        "after": "2024-01-18",
        "before": "2024-05-15"
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
}

{
  "operation_name": "ChangeGearbox",
  "arguments": {
    "level": 25,
    "meteo": { "town": "Chambon" }
}
}
```

4. Run the tests with `pytest`

4 files and 20 tests.
- test_app : test the endpoints of the fastapi (post opration and validation)
- test_check_service : test the @date, @level and @meteo
- test_restrictions_service : test the recursivity of the algo
- test_weather_service: test rest call to openweathermap

5. Next steps

- add database => s3 is a good choice to store the json operations
- create dockerfile
- add a .gitlab-ci.yml
- deploy on AWS