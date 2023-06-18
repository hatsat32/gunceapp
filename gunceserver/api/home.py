from fastapi import APIRouter


r = APIRouter()


@r.get("/")
def root():
    return {"msg": "Hello World from GunceApp!"}


@r.get("/api/ping")
def ping_pong():
    return {"ping": "pong!"}
