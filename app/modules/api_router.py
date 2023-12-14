from fastapi import APIRouter

from app.core.config import setting
from app.modules.auth import auth_api

router = APIRouter()


# router.include_router(
#     pet_api.router, prefix=setting.APP_V1_STR + "/pet", tags=["Pet"]
# )
router.include_router(
    auth_api.router, prefix=setting.APP_V1_STR + "/auth", tags=["Auth"]
)
