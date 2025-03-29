from core.config import Settings
from fastapi import Depends, HTTPException
import aiohttp
import asyncio
from urllib.parse import unquote
import datetime as dt

async def get_region_data(settings:Settings):

    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/areaCode1"
    # 루트 지역부터 설정!
    root_region = await get_root_region(api_key, url)

    return root_region



async def get_root_region(api_key:str, url:str):
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : 100,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "_type" : "json",        # 응답 타입
        # 지역 코드
    }
    result = []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                item_list = data.get("response", {}).get("body",{}).get("items",{}).get("item",{})
                if item_list:
                    for item in item_list:
                        region_data = {
                            "region_code": item.get("code",""),
                            "region_name": item.get("name"),

                        }
                        result.append(region_data)
                else:
                    raise HTTPException(status_code=404, detail="Item not found in the response")  # 아이템이 없을 경우
                return result
                
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 