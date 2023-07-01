import random
from starlette.testclient import TestClient

randuser = random.randint(100, 1000)

login_jwt = None


class TestEntryAPI:
    test_data = {
        "date": "2023-06-23",
        "title": "BBBBBBBBBBBBBBBBBB",
        "title_key_tag": "b7d793b5b4ac76e31e5c30d1",
        "title_key_nonce": "dacd3fffafda3d79cf4bf36fc6d84b74",
        "content": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "content_key_tag": "b7d793b5b4ac76e31e5c30d1",
        "content_key_nonce": "dacd3fffafda3d79cf4bf36fc6d84b74",
    }

    def test_login(self, test_app: TestClient):
        data = {
            "username": "user_1",
            "serverkey": "ee101456183efc93c2ebf8d23cb2914b36598e295d9e8a137ba852d53f87a3fa",  # noqa: E501
        }
        response = test_app.post("/api/auth/login", json=data)
        global login_jwt
        login_jwt = response.json()["access_token"]
        assert response.status_code == 200

    def test_create_entry_unauthorized(self, test_app: TestClient):
        response = test_app.post("/api/entries", json=self.test_data)
        assert response.status_code == 401

    def test_create_entry(self, test_app: TestClient):
        response = test_app.post(
            "/api/entries",
            json=self.test_data,
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        assert response.status_code == 201

    def test_list_entry(self, test_app: TestClient):
        response = test_app.get(
            "/api/entries",
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        assert response.status_code == 200

    def test_entry_detail(self, test_app: TestClient):
        response = test_app.get(
            "/api/entries",
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        uuid = response.json()[0]["id"]

        response = test_app.get(
            f"/api/entries/{uuid}",
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        assert response.status_code == 200

    def test_entry_update(self, test_app: TestClient):
        response = test_app.get(
            "/api/entries",
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        uuid = response.json()[0]["id"]

        testdata = self.test_data.copy()
        testdata["title"] = "AASSDDFF"
        response = test_app.put(
            f"/api/entries/{uuid}",
            json=testdata,
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        assert response.status_code == 200

    def test_entry_delete(self, test_app: TestClient):
        response = test_app.get(
            "/api/entries",
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        uuid = response.json()[0]["id"]

        response = test_app.delete(
            f"/api/entries/{uuid}",
            headers={"Authorization": f"Bearer {login_jwt}"},
        )
        print(response.json())
        assert response.status_code == 200
