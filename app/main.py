from typing import Union
import uvicorn
from functools import lru_cache
from fastapi import Depends, FastAPI, HTTPException, Query
from typing_extensions import Annotated
from core import config

from openapi.getMuseum import get_museum_data  
from openapi.getAreaCode import get_area_code

app = FastAPI(swagger_ui_parameters={"syntaxHighlight":True})

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
        museums = await get_museum_data(numOfRows, settings)
        print(len(museums))
        return museums
    except Exception as e:
        print()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/areaCode")
async def get_museum(
    numOfRows:int =  Query(3, description="장소 코드 통합 조회"),
    settings: config.Settings = Depends(get_settings)
):
    try:
        museums = await get_museum_data(numOfRows, settings)
        print(len(museums))
        return museums
    except Exception as e:
        print()
        raise HTTPException(status_code=500, detail=str(e))

# main 함수에서 환경 설정 값을 사용
def main():
    settings = get_settings()  # 캐싱된 설정 값 사용
    uvicorn.run("main:app", host="0.0.0.0", port=int(settings.EXTERNAL_PORT), reload=True)

if __name__ == "__main__":
    main()
    