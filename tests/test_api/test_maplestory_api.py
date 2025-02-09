from api import MaplestoryAPI
import unittest

class TestLunchRepository(unittest.TestCase):
    def setUp(self):
        self.maple_api = MaplestoryAPI()
        
    def test_get_nexon_to_ocid(self):
        characterName = "빵먹는비숍"
        ocid = self.maple_api.get_nexon_to_ocid(characterName)
        print(ocid)

    def test_get_nexon_maplebasic(self):
        characterName = "빵먹는비숍"
        ocid = self.maple_api.get_nexon_to_ocid(characterName)
        maple_basic = self.maple_api.get_nexon_maplebasic(ocid.ocid)
        print(maple_basic)

if __name__ == "__main__":
    unittest.main()
    
