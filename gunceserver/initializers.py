from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

from api import api_routes, public_router, auth_router
from core.exceptions import HTTPException
from core.deps import get_settings


def init_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(api_routes)
    app.include_router(public_router)


def init_cors(app: FastAPI):
    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_exceptions(app: FastAPI):
    @app.exception_handler(HTTPException)
    def app_exception_handler(exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            {"detail": exc.detail, "message": exc.message},
            status_code=exc.status_code,
            headers=exc.headers,
        )


def init(app: FastAPI):
    init_routes(app)
    init_cors(app)
    init_exceptions(app)


def create_app(version: str) -> FastAPI:
    s = get_settings()

    application = FastAPI(
        title=s.APP_NAME,
        description=s.DESCRIPTION,
        debug=s.DEBUG,
        version=version,
        openapi_url=s.OPENAPI_URL,
    )

    init(application)

    return application


def create_app(version: str) -> FastAPI:
    s = get_settings()

    application = FastAPI(
        title=s.APP_NAME,
        description=s.DESCRIPTION,
        debug=s.DEBUG,
        version=version,
        openapi_url=s.OPENAPI_URL,
    )

    init(application)

    return application
