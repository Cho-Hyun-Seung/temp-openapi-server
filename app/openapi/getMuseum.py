from core.config import Settings
from fastapi import Depends, HTTPException
import aiohttp
import asyncio
from urllib.parse import unquote
import datetime as dt


async def get_museum_data(settings:Settings):
    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/areaBasedSyncList1"
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : 10000,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "contentTypeId" : 14,
        "_type" : "json",        # 응답 타입
        "cat1": "A02",
        "cat2" : "A0206",
        "cat3" : "A02060100"
    }
    result = []


    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                item_list = data.get("response", {}).get("body",{}).get("items",{}).get("item",{})
                if item_list:
                #    item = item_list[0]
                   result = [
                       {
                            "title": item.get("title","No Title"),
                            "first_image": item.get("firstimage", ""),
                            "addr1": item.get("addr1", "No Address"),
                            "addr2":item.get("addr2"),
                            "content_id": item.get("contentid", None),
                        } for item in item_list]
                else:
                    raise HTTPException(status_code=404, detail="Item not found in the response")  # 아이템이 없을 경우
                return result
                
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 