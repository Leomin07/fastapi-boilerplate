from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ""
    message: str = ""

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = "000"
        self.message = "Successfully"
        return self


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 400
        self.code = code if code else str(self.http_code)
        ## TODO: add dev message
        self.message = message


async def http_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(
            ResponseSchemaBase().custom_response(exc.code, exc.message)
        ),
    )
