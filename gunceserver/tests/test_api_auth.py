import random
import json
from base64 import b64decode
from starlette.testclient import TestClient


class TestAuthAPI:
    test_data = {
        "username": "user_1",
        "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",
        "masterkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",
        "nonce": "b7d793b5b4ac76e31e5c30d1",
        "tag": "dacd3fffafda3d79cf4bf36fc6d84b74",
    }

    def test_register(self, test_app: TestClient):
        response = test_app.post("/api/auth/register", json=self.test_data)
        assert response.status_code == 200

    def test_login(self, test_app: TestClient):
        response = test_app.post(
            "/api/auth/login",
            json={
                "username": "user_1",
                "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",
            },
        )

        assert response.status_code == 200

        jwtbody = b64decode(response.json()["access_token"].split(".")[1] + "==")
        user = json.loads(jwtbody.decode())["username"]
        assert user == "user_1"

    def test_login_with_wrong_credentials(self, test_app: TestClient):
        response = test_app.post(
            "/api/auth/login",
            json={
                "username": "user_2",
                "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",
            },
        )
        assert response.status_code == 401
