import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "PahadRakshak"
    APP_SUBTITLE: str = "AI-Powered Disaster Risk Intelligence & Emergency Response Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "127.0.0.1"

    DATABASE_URL: str = "sqlite:///./pahadrakshak.db"

    SECRET_KEY: str = "pahadrakshak_secret_key_techforge_3_0_srhu"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # SIH 2026 Problem Statement Adaptability
    SIH_PROBLEM_ID: str = "SIH-PROVISIONAL-DISASTER-01"
    SIH_PROBLEM_TITLE: str = "AI-Assisted Disaster Risk Intelligence & Emergency Response"
    SIH_ORGANIZATION: str = "NDMA / State Disaster Management Authority"
    SIH_THEME: str = "Disaster Management & Mountain Safety"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
