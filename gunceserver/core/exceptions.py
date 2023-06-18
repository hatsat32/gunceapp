from typing import Any, Optional, Dict
from fastapi import HTTPException as FastAPIHTTPException
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)


class HTTPException(FastAPIHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        message: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.message = message


HTTP_404_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Item not found",
    message="The item you are looking for is not found.",
)

HTTP_401_UNAUTHORIZED_EXCEPTION = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Unauthorized",
    message="You must login to access this page.",
)

HTTP_403_FORBIDDEN_EXCEPTION = HTTPException(
    status_code=HTTP_403_FORBIDDEN,
    detail="Forbidden",
    message="You do not have enough permissions to access this page.",
)

HTTP_400_BAD_REQUEST_EXCEPTION = HTTPException(
    status_code=HTTP_400_BAD_REQUEST, detail="Bad request", message="Bad request"
)

HTTP_409_CONFLICT_EXCEPTION = HTTPException(
    status_code=HTTP_409_CONFLICT, detail="Conflict", message="The data already exists"
)
