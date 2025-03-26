from core.config import Settings
from fastapi import Depends, HTTPException
import aiohttp
import asyncio
from urllib.parse import unquote
import datetime as dt


async def get_museum_data(numOfRows:int, settings:Settings):
    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/areaBasedSyncList1"
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : numOfRows,
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
                   for item in item_list:
                       museum_data = {
                          "title": item.get("title","No Title"),
                            "first_image": item.get("firstimage", ""),
                            "addr1": item.get("addr1", "No Address"),
                            "addr2":item.get("addr2"),
                            "content_id": item.get("contentid", None),
                       }
                       museum_detail = await get_museum_detail(museum_data.get("content_id"), settings)
                       museum_overview = await get_museum_overview(museum_data.get("content_id"), settings)
                       museum_data.update(museum_detail)
                       museum_data.update(museum_overview)
                       result.append(museum_data)
                else:
                    raise HTTPException(status_code=404, detail="Item not found in the response")  # 아이템이 없을 경우
                return result
                
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 
    
async def get_museum_detail(contentId: str, settings:Settings):
    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/detailIntro1"
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : 100,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "contentTypeId" : 14,
        "contentId" : contentId,
        "_type" : "json",        # 응답 타입
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                item = data.get("response", {}).get("body",{}).get("items",{}).get("item",{})[0]
                museum_detail_data = {
                    "discount_info": item.get("discountinfo",""),   # 할인 정보
                    "use_fee" : item.get("usefee",""),   # 이용 요금
                    "rest_date" : item.get("restdateculture", "") # 쉬는 날날
                }
                return museum_detail_data
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 
    

async def get_museum_overview(contentId, settings:Settings):
    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/detailCommon1"
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : 100,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "contentTypeId" : 14,
        "contentId" : contentId,
        "_type" : "json",        # 응답 타입
        "defaultYN" : "N",  # 기본 응답
        "firstImageYN" : "N", # 대표 이미지
        "areacodeYN" : "N", # 지역 코드
        "catcodeYN" : "N",  # 서비스 분류 코드 (대, 중, 소)
        "addrinfoYN" : "N", # 주소 조회
        "mapinfoYN" : "N",   # 좌표 조회
        "overviewYN" : "Y"  # 개요 조회

    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                item = data.get("response", {}).get("body",{}).get("items",{}).get("item",{})[0]
                museum_overview = {
                    "overview": item.get("overview",""),   # 개요
                }
                return museum_overview
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 