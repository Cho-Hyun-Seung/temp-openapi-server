from core.config import Settings
from fastapi import Depends, HTTPException
import aiohttp
import asyncio
from urllib.parse import unquote
import datetime as dt


async def get_place_data(numOfRows:int,contentTypeId:int, cat2:str, cat3:str,settings:Settings):
    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/areaBasedSyncList1"
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : numOfRows,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "contentTypeId" : contentTypeId,
        "_type" : "json",        # 응답 타입
        "cat1": "A02",
        "cat2" : cat2,
        "cat3" : cat3
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
                       place_data = {
                          "title": item.get("title","No Title"),
                            "first_image": item.get("firstimage", ""),
                            "addr1": item.get("addr1", "No Address"),
                            "addr2":item.get("addr2"),
                            "content_id": item.get("contentid", None),
                       }
                       place_detail = await get_place_detail(place_data.get("content_id"),contentTypeId ,settings)
                       place_overview = await get_place_overview(place_data.get("content_id"), settings)
                       place_data.update(place_detail)
                       place_data.update(place_overview)
                       result.append(place_data)
                else:
                    raise HTTPException(status_code=404, detail="Item not found in the response")  # 아이템이 없을 경우
                return result
                
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 
    
async def get_place_detail(contentId: str, contentTypeId:int, settings:Settings):
    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/detailIntro1"
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : 100,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "contentTypeId" : contentTypeId,
        "contentId" : contentId,
        "_type" : "json",        # 응답 타입
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                item = data.get("response", {}).get("body",{}).get("items",{}).get("item",{})[0]
                place_detail_data = {}
                if contentTypeId == 14:
                    place_detail_data = {
                        "discount_info": item.get("discountinfo",""),   # 할인 정보
                        "use_fee" : item.get("usefee",""),   # 이용 요금
                        "rest_date" : item.get("restdateculture", "") # 쉬는 날
                    }
                else:
                    place_detail_data = {
                        "rest_date": item.get("restdate",""),   # 쉬는 날
                    }


                return place_detail_data
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out")


async def get_place_overview(contentId, settings:Settings):
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
                place_overview = {
                    "overview": item.get("overview",""),   # 개요
                }
                return place_overview
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")  # 예외 처리
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out") 