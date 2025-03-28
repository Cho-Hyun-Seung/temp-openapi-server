from core.config import Settings
from fastapi import Depends, HTTPException
import aiohttp
import asyncio
from urllib.parse import unquote
import datetime as dt

async def get_area_code(settings:Settings):
    api_key = unquote(settings.OPEN_API_KEY)
    url = "http://apis.data.go.kr/B551011/KorService1/areaCode1"
        params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows" : 10000,
        "MobileOS": "ETC",
        "MobileApp" : "GulHan",
        "contentTypeId" : 14,
        "_type" : "json",        # 응답 타입
        # 지역 코드
    }