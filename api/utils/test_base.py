import unittest2 as unittest
from main import create_app
from api.utils.database import db
import tempfile


class BaseTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app = create_app('testing')
        # self.test_db_file = tempfile.mkstemp()[1]
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        with app.app_context():
            db.create_all()
        app.app_context().push()
        self.app = app.test_client()

    def tearDown(self) -> None:
        db.close_all_sessions()
        db.drop_all()
