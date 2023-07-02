import json
from base64 import b64decode
from starlette.testclient import TestClient

login_jwt = None

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
                "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",  # noqa: E501
            },
        )

        assert response.status_code == 200

        jwtbody = b64decode(response.json()["access_token"].split(".")[1] + "==")
        user = json.loads(jwtbody.decode())["username"]
        assert user == "user_1"

    def test_login_with_wrong_credentials(self, test_app: TestClient):
        # test with wron username
        response = test_app.post(
            "/api/auth/login",
            json={
                "username": "user_2",
                "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",  # noqa: E501
            },
        )
        assert response.status_code == 401

        # test with wrong password
        response = test_app.post(
            "/api/auth/login",
            json={
                "username": "user_1",
                "serverkey": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # noqa: E501
            },
        )
        assert response.status_code == 401

    def test_change_password(self, test_app: TestClient):
        # first login
        login_data = {
            "username": "user_1",
            "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",  # noqa: E501
        }
        response = test_app.post("/api/auth/login", json=login_data)
        login_jwt: str = response.json()["access_token"]
        assert response.status_code == 200

        # chagne pass
        chpass_data = {
            "serverkey": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "masterkey": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "nonce": "cccccccccccccccccccccccc",
            "tag": "dddddddddddddddddddddddddddddddd"
        }
        response = test_app.post(
            "/api/auth/change-password",
            json=chpass_data,
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        assert response.status_code == 204

        # login with new creds
        new_login_data = {
            "username": "user_1",
            "serverkey": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # noqa: E501
        }
        response = test_app.post("/api/auth/login", json=new_login_data)
        # login_jwt: str = response.json()["access_token"]
        assert response.status_code == 200


    def test_auth_me(self, test_app: TestClient):
        # first login
        login_data = {
            "username": "user_1",
            "serverkey": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",  # noqa: E501
        }
        response = test_app.post("/api/auth/login", json=login_data)
        login_jwt: str = response.json()["access_token"]
        assert response.status_code == 200

        response = test_app.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        res_json = response.json()
        assert response.status_code == 200
        assert res_json["username"] == "user_1"
