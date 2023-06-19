import random
import json
from base64 import b64decode

from fastapi.testclient import TestClient

from main import app

randuser = random.randint(100, 1000)

client = TestClient(app)


def test_register():
    data = {
        "username": "user_" + str(randuser),
        "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",
        "masterkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",
        "nonce": "b7d793b5b4ac76e31e5c30d1",
        "tag": "dacd3fffafda3d79cf4bf36fc6d84b74",
    }
    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 200


def test_login():
    data = {
        "username": "user_" + str(randuser),
        "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",
    }
    response = client.post("/api/auth/login", json=data)
    assert response.status_code == 200
    user = json.loads(
        b64decode(response.json()["access_token"].split(".")[1] + "==").decode()
    )["username"]
    assert user == "user_" + str(randuser)
