import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Settings(BaseModel):
    # =====================================================
    # DATABASE
    # =====================================================

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # =====================================================
    # FRONTEND / CORS
    # =====================================================

    FRONTEND_URL: str
    ALLOWED_ORIGINS: str

    # =====================================================
    # DATABASE URL
    # =====================================================

    @property
    def DATABASE_URL(self) -> str:
        user = quote_plus(self.DB_USER)
        password = quote_plus(self.DB_PASSWORD)

        return (
            f"postgresql://{user}:{password}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings(
    # =====================================================
    # DATABASE
    # =====================================================

    DB_HOST=os.getenv(
        "DB_HOST",
        "localhost",
    ),

    DB_PORT=int(
        os.getenv(
            "DB_PORT",
            "5432",
        )
    ),

    DB_NAME=os.getenv(
        "DB_NAME",
        "",
    ),

    DB_USER=os.getenv(
        "DB_USER",
        "",
    ),

    DB_PASSWORD=os.getenv(
        "DB_PASSWORD",
        "",
    ),

    # =====================================================
    # FRONTEND / CORS
    # =====================================================

    FRONTEND_URL=os.getenv(
        "FRONTEND_URL",
        "http://localhost:3000",
    ),

    ALLOWED_ORIGINS=os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ),
)