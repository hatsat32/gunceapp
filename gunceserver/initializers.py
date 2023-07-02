from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import public_router, auth_router, entry_router
from core.deps import get_settings


def init_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(entry_router)
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


def init(app: FastAPI):
    init_routes(app)
    init_cors(app)


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
