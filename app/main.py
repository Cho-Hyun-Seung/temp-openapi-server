from typing import Union
import uvicorn
from functools import lru_cache
from fastapi import Depends, FastAPI, HTTPException, Query
from typing_extensions import Annotated
from core import config
from core.database import get_session
from sqlalchemy.orm import Session

from openapi.getPlace import get_place_data  
from openapi.getAreaCode import get_region_data

app = FastAPI(swagger_ui_parameters={"syntaxHighlight":True})
SessionDep = Annotated[Session, Depends(get_session)]

@lru_cache
def get_settings():
    return config.Settings()


@app.get("/")
def read_root():
    return {"Hello": "world12"}


@app.get("/museum")
async def get_museum(
    numOfRows:int =  Query(3, description="한번에 받아올 박물관 개수"),
    settings: config.Settings = Depends(get_settings)
):
    try:
        museums = await get_place_data(numOfRows,14,'A0206','A02060100', settings)
        print(len(museums))
        return museums
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/historicsite")
async def get_historic_site(
    numOfRows:int =  Query(3, description="한번에 받아올 유적지 개수"),
    settings: config.Settings = Depends(get_settings)
):
    try:
        historicsite = await get_place_data(numOfRows, 12,'A0201','A02010700', settings)
        print(len(historicsite))
        return historicsite
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/folkvillage")
async def get_folk_village(
    numOfRows:int =  Query(3, description="한번에 받아올 민속마을 개수"),
    settings: config.Settings = Depends(get_settings)
):
    try:
        folk_village = await get_place_data(numOfRows, 12, 'A0201','A02010600', settings)
        print(len(folk_village))
        return folk_village
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/region")
async def get_region(
    session: SessionDep,
    settings: config.Settings = Depends(get_settings)
):
    try:
        regions = await get_region_data(settings, session)
        print(len(regions))
        return regions
    except Exception as e:
        print()
        raise HTTPException(status_code=500, detail=str(e))

# main 함수에서 환경 설정 값을 사용
def main():
    settings = get_settings()  # 캐싱된 설정 값 사용
    uvicorn.run("main:app", host="0.0.0.0", port=int(settings.EXTERNAL_PORT), reload=True)

if __name__ == "__main__":
    main()
    