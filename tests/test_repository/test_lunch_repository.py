import unittest

from data.entity import Lunch
from data.repository import LunchRepository
from data.provider import SessionProvider

class TestLunchRepository(unittest.TestCase):
    def setUp(self):
        self.provider = SessionProvider()
        self.lunch_repository = LunchRepository(self.provider)
        
    def test_insert_lunch(self):
        lunch = Lunch(lunch = "김치찌개")
        self.lunch_repository.save_lunch(lunch)
        
    def test_get_random_lunch_test(self):
        lunch = self.lunch_repository.get_random_lunch()
        print(lunch)


if __name__ == "__main__":
    unittest.main()