from typing import Union
import uvicorn
from functools import lru_cache
from fastapi import Depends, FastAPI, HTTPException
from typing_extensions import Annotated
from core import config

from openapi.getMuseum import get_museum_data  

app = FastAPI()

@lru_cache
def get_settings():
    return config.Settings()


@app.get("/")
def read_root():
    return {"Hello": "world12"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/museum")
async def get_museum(
    settings: config.Settings = Depends(get_settings)
):
    # try:
    museums = await get_museum_data(settings)
    print(len(museums))
    return museums
    # except Exception as e:
    #     print()
    #     raise HTTPException(status_code=500, detail=str(e))

# main 함수에서 환경 설정 값을 사용
def main():
    import multiprocessing
    multiprocessing.freeze_support()
    settings = get_settings()  # 캐싱된 설정 값 사용
    uvicorn.run("main:app", host="0.0.0.0", port=int(settings.EXTERNAL_PORT), reload=True)

if __name__ == "__main__":
    main()
    