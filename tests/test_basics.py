# -*- coding: utf-8 -*-
import unittest
import time
from flask import current_app
from app import create_app, DB
from app.models import User

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        DB.create_all()

    def tearDown(self):
        DB.session.remove()
        DB.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

