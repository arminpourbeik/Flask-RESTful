import json
from api.utils.test_base import BaseTestCase
from api.models.author import Author
from api.models.book import Book
from datetime import datetime
from flask_jwt_extended import create_access_token
import unittest2 as unittest
import io


def create_authors():
    author1 = Author(first_name='John', last_name='Doe').create()
    author2 = Author(first_name='Jane', last_name='Doe').create()


def login():
    access_token = create_access_token(identity='kunal.relan@hotmail.com')
    return access_token


class TestAuthors(BaseTestCase):
    def setUp(self) -> None:
        super(TestAuthors, self).setUp()
        create_authors()

    def test_create_author(self):
        token = login()
        author = {'first_name': 'Johny', 'last_name': 'Doee'}
        response = self.app.post('/api/authors/', data=json.dumps(author), content_type='application/json',
                                 headers={'Authorization': f'Bearer {token}'})
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('author' in data)

    def test_create_author_no_authorization(self):
        author = {'first_name': 'Johny', 'last_name': 'Doee'}
        response = self.app.post('/api/authors/', data=json.dumps(author), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(401, response.status_code)

    def test_upload_avatar(self):
        token = login()
        response = self.app.post(
            '/api/authors/avatar/2',
            data=dict(avatar=(io.BytesIO(b'test'), 'test_file.jpg')),
            content_type='multipart/form-data',
            headers={'Authorization': 'Bearer ' + token}
        )
        self.assertEqual(200, response.status_code)

    def test_upload_with_csv_file(self):
        token = login()
        response = self.app.post(
            '/api/authors/avatar/2',
            data=dict(avatar=(io.BytesIO(b'test'), 'test_file.csv')),
            content_type='multipart/form-data',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(422, response.status_code)

    def test_get_authors(self):
        response = self.app.get(
            '/api/authors/',
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('authors' in data)

    def test_get_author_detail(self):
        response = self.app.get(
            '/api/authors/2',
            content_type='application/json'
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('author' in data)


if __name__ == '__main__':
    unittest.main()
