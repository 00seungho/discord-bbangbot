import unittest

from data.service import LunchService
from data.provider import SessionProvider
from data.repository import LunchRepository

class TestLunchService(unittest.TestCase):
    def setUp(self):
        self.provider = SessionProvider()
        self.lunch_repository = LunchRepository(self.provider)
        self.lunch_service = LunchService(self.lunch_repository)

    def test_get_random_menu(self):
        print(self.lunch_service.get_random_menu())

