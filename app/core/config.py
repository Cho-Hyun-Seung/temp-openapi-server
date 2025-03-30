from fastapi import FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OpenApiServer"
    OPEN_API_KEY: str
    EXTERNAL_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    DB_PORT: int

    model_config = SettingsConfigDict(env_file=".env")


# settings = Settings()
# app = FastAPI()


# @app.get("/info")
# async def info():
#     return {
#         "app_name": settings.app_name,
#     }