from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import setting
from app.core.exception_handler import CustomException, http_exception_handler
from app.modules.api_router import router

app = FastAPI(title=setting.APP_NAME, openapi_url=f"{setting.APP_V1_STR}/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=setting.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(CustomException, http_exception_handler)

app.include_router(router)
