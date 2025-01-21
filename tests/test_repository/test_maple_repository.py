import unittest

from data.entity import Mapleocid,Maplebasic
from data.repository import MapleRepository
from data.provider import SessionProvider
import requests
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
import os

class TestMapleRepository(unittest.TestCase):
    def setUp(self):
        self.provider = SessionProvider()
        self.maple_repository = MapleRepository(self.provider)
        self.character_name = "빵먹는비숍"
        load_dotenv()
        self.api_key = os.getenv("nexonapi")
        self.headers = {
         "x-nxopen-api-key": self.api_key
        }

    def test_save_ocid(self):
        print("-------------test_save_ocid----------")
        urlString = f"https://open.api.nexon.com/maplestory/v1/id?character_name={self.character_name}"
        response = requests.get(urlString, headers = self.headers)
        try:
            if response.status_code == 200:
                ocid = Mapleocid(ocid = response.json()['ocid'],
                                 nickname = self.character_name)
                self.maple_repository.save_ocid(ocid)
                print("ocid 삽입 성공")
            else:
                raise Exception(f"{response.json()['error']['name']}")
        except Exception as e:
            return e
        
    def test_get_by_nick_name(self):
        print("-------------test_get_by_nick_name----------")
        ocid = self.maple_repository.get_by_nick_name(self.character_name)
        print(ocid)

    def test_save_maplebasic(self):
        print("-------------test_save_maplebasic----------")
        ocid = self.maple_repository.get_by_nick_name(self.character_name)
        ocid_str = ocid.ocid
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        basicUrlString = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid_str}&date={yesterday}"
        unionUrlString = f"https://open.api.nexon.com/maplestory/v1/user/union?ocid={ocid_str}&date={yesterday}"
        dojangUrlString = f"https://open.api.nexon.com/maplestory/v1/character/dojang?ocid={ocid_str}&date={yesterday}"
        try:
            responseBasic = requests.get(basicUrlString, headers = self.headers)
            responseUnion = requests.get(unionUrlString,headers= self.headers)
            responseDojang = requests.get(dojangUrlString,headers= self.headers)
            if responseBasic.status_code == 200 and responseUnion.status_code == 200 and responseDojang.status_code == 200:
                level = int(responseBasic.json()["character_level"])
                date = datetime.fromisoformat(responseBasic.json()["date"])
                guild_name = responseBasic.json()["character_guild_name"]
                image = responseBasic.json()["character_image"]
                C_class = responseBasic.json()["character_class"]
                unionLv = int(responseUnion.json()["union_level"])
                dojang = int(responseDojang.json()["dojang_best_floor"])
                maplebasic = Maplebasic(
                    level = level,
                    date = date,
                    guild_name = guild_name,
                    image = image,
                    unit_class = C_class,
                    union_lv = unionLv,
                    dojang = dojang,
                    ocid = ocid_str
                )
                self.maple_repository.save_maplebasic(maplebasic)
                print(maplebasic)
                print("maplebasic 삽입 완료")
        except Exception as e:
            print(e)
            return e
        
        
        

    def test_get_by_ocid(self):
        print("-------------test_get_by_ocid----------")

        ocid = self.maple_repository.get_by_nick_name(self.character_name)
        ocid_str = ocid.ocid
        maple_basic = self.maple_repository.get_by_ocid(ocid_str)
        print(maple_basic)

if __name__ == "__main__":
    unittest.main()