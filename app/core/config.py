from typing import List, Union, Annotated, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, field_validator, BeforeValidator


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Backend"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "f3e7b9a5c2d8e1f4b0a7d9c6e3b2a5f1d4c7b0e9a2d5f8b1c4e7d0a3f6b9c2"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://student_db_qoou_user:D34DjKZetKeIQtMomUabBuLIxjOIFIYx@dpg-d5do7jbuibrs7394m4o0-a.virginia-postgres.render.com/student_db_qoou"

    # External Services
    REMOVE_BG_API_KEY: str = "APY0sAmUXNYKR7XRZXyUiH401IXCqjtlEgWxAgOFgJTyd4KQkdcBIC34DzEw1av5IjKE9g8se"

    # CORS
    BACKEND_CORS_ORIGINS: Any = ["https://react-api-frontend-weld.vercel.app"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str):
            if not v.startswith("["):
                return [i.strip() for i in v.split(",") if i.strip()]
            else:
                import json

                try:
                    return json.loads(v)
                except:
                    return v
        return v

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


settings = Settings()
