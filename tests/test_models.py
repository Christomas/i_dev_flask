from app.models import User
from tests.test_basics import BaseTestCase


class UserModelTestCase(BaseTestCase):
    def test_no_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_setter(self):
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_check_password(self):
        u = User(password='cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='dog')
        self.assertTrue(u.password_hash!=u2.password_hash)
