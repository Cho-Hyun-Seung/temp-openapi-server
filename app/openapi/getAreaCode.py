from core.config import Settings
from fastapi import Depends, HTTPException
import aiohttp
import asyncio
from urllib.parse import unquote
import datetime as dt

async def get_region_data(settings:Settings):

    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/areaCode1"

    # 루트 지역 생성성
    region_list:list = await get_root_region(api_key, url)
    child_region_list:list = []

    # 루트 지역을 순회하며 자식 지역 생성
    for root_region in region_list:
        child_region_list.extend(
            await get_child_region(api_key, url, root_region))
    
    # 루트 지역 정보 + 자식 지역 정보
    region_list.extend(child_region_list)


    return region_list



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
                            "region_name": item.get("name",""),
                            "parent_region_name" : None

                        }
                        result.append(region_data)
                else:
                    raise HTTPException(status_code=404, detail="Item not found in the response")  # 아이템이 없을 경우
                return result
                
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 

async def get_child_region(api_key:str, url:str, root_region):
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : 100,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "_type" : "json",       # 응답 타입
        "areaCode": root_region.get("region_code")     # 지역 코드
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
                            "parent_region_name" : root_region.get("region_name")

                        }
                        result.append(region_data)
                else:
                    raise HTTPException(status_code=404, detail="Item not found in the response")  # 아이템이 없을 경우
                return result
                
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 