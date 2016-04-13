import time

from tests.test_basics import BaseTestCase
from app import options


class OptionsTestCase(BaseTestCase):
    def test_valid_token(self):
        token = options.dump_token('id', 'cat')
        self.assertTrue(options.load_token(token, 'id')=='cat')

    def test_invalid_token(self):
        token = options.dump_token('dog', 3)
        self.assertFalse(options.load_token(token, 'cat')==3)
        self.assertFalse(options.load_token(token, 'dog')==4)

    def test_expired_token(self):
        token = options.dump_token('cat', 3, expires_in=1)
        time.sleep(2)
        self.assertFalse(options.load_token(token, 'cat')==3)
