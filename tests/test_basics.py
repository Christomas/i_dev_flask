from unittest import TestCase

from flask import current_app

from app import create_app, db


class BaseTestCase(TestCase):
    """测试基类。"""
    def setUp(self):
        """测试准备。"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """测试清理。"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


class AppTestCase(BaseTestCase):
    """基本测试。"""
    def test_app_exists(self):
        """测试当前app存在。"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """测试当前app为测试模式。"""
        self.assertTrue(current_app.config['TESTING'])
