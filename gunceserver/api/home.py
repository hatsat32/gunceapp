from typing import Dict

from fastapi import APIRouter


r = APIRouter()


@r.get("/", response_model=Dict[str, str])
def root():
    return {"msg": "Hello World from GunceApp!"}


@r.get("/api/ping", response_model=Dict[str, str])
def ping_pong():
    return {"ping": "pong!"}
