import json
from api.utils.test_base import BaseTestCase
from api.models.user import User
from datetime import datetime
import unittest2 as unittest
from api.utils.token import generate_verification_token, confirm_verification_token


def create_users():
    user1 = User(
        email="kunal.relan12@gmail.com",
        username="kunalrelan12",
        password=User.generate_hash("helloworld"),
        is_verified=True,
    ).create()
    user2 = User(
        email="kunal.relan123@gmail.com",
        username="kunalrelan125",
        password=User.generate_hash("helloworld"),
    ).create()


class TestUsers(BaseTestCase):
    def setUp(self) -> None:
        super(TestUsers, self).setUp()
        create_users()

    def test_login_user(self):
        user = {"email": "kunal.relan12@gmail.com", "password": "helloworld"}
        response = self.app.post(
            "/api/users/login", data=json.dumps(user), content_type="application/json"
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access_token" in data)

    def test_login_user_wrong_credentials(self):
        user = {"email": "kunal.relan12@gmail.com", "password": "helloworld12"}
        response = self.app.post(
            '/api/users/login', data=json.dumps(user), content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(401, response.status_code)

    def test_login_unverified_user(self):
        user = {
            'email': 'kunal.relan123@gmail.com',
            'password': 'helloworld'
        }
        response = self.app.post(
            '/api/users/login', data=json.dumps(user), content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(400, response.status_code)


if __name__ == "__main__":
    unittest.main()
