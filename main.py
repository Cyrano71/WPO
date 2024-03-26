import uvicorn
import asyncio
from fastapi import FastAPI
from app.routers import operations
import configparser

app = FastAPI()
app.include_router(operations.router)

@app.get("/")
def root():
    return {"message": "Fast API in Python"}
    
async def main():
    config = configparser.ConfigParser()
    config.read("config.ini")
    await operations.build(config)
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())