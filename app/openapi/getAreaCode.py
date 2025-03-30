from typing import Optional
from core.config import Settings
from fastapi import HTTPException
import aiohttp
import asyncio
from urllib.parse import unquote
from models.region import Region
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

async def get_region_data(settings: Settings, session: AsyncSession):
    try:
        api_key = unquote(settings.OPEN_API_KEY)
        url = "http://apis.data.go.kr/B551011/KorService1/areaCode1"

        # 1. 루트 지역 수집
        root_region_list: list = await get_root_region(api_key, url)

        # 2. 자식 지역 수집
        child_region_list: list = []
        for root_region in root_region_list:
            try:
                children = await get_child_region(api_key, url, root_region)
                child_region_list.extend(children)
            except Exception as e:
                print(f"[자식 지역 로드 실패] {root_region} - {e}")

        # 3. 루트 지역 insert

        # 4. 자식 지역 insert

        # 5. 전체 리스트 반환
        all_region_list = root_region_list + child_region_list
        return all_region_list

    except Exception as e:
        print(f"[전체 오류] 지역 데이터 처리 중 예외 발생: {e}")
        raise



async def get_root_region(api_key: str, url: str):
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 100,
        "MobileOS": "ETC",
        "MobileApp": "GulHan",
        "_type": "json"
    }
    result = []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                item_list = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
                for item in item_list:
                    region_data = {
                        "region_code": item.get("code", ""),
                        "region_name": item.get("name", ""),
                        "parent_region_name": None
                    }
                    result.append(region_data)
                return result

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out")


async def get_child_region(api_key: str, url: str, root_region):
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 100,
        "MobileOS": "ETC",
        "MobileApp": "GulHan",
        "_type": "json",
        "areaCode": root_region.get("region_code")
    }
    result = []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                item_list = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
                for item in item_list:
                    region_data = {
                        "region_code": item.get("code", ""),
                        "region_name": item.get("name", ""),
                        "parent_region_name": root_region.get("region_name")
                    }
                    result.append(region_data)
                print(result)
                return result

    except aiohttp.ClientError as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Request timed out")
