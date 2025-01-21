import unittest

from data.entity import Maplebasic,Mapleocid
from data.service import MapleService
from data.provider import SessionProvider
from data.repository import MapleRepository
from datetime import datetime, timedelta,timezone
from data.dto import MapleBasicDTO, OcidDTO
from dotenv import load_dotenv
import os
from tests.log import FunLog
import requests


class TestLunchService(unittest.TestCase):
    def setUp(self):
        self.provider = SessionProvider()
        self.maple_repository = MapleRepository(self.provider)
        self.maple_service = MapleService(self.maple_repository)
        self.nickname = ""
        self.character_name = "빵먹달"
        load_dotenv()
        self.api_key = os.getenv("nexonapi")
        self.headers = {
         "x-nxopen-api-key": self.api_key
        }

    @FunLog()
    def test_get_ocid(self):
        print(self.maple_service.get_ocid(self.nickname))


    @FunLog()
    def test_get_maple_basic(self):
        ocid = self.maple_service.get_ocid(self.nickname).ocid
        print(self.maple_service.get_maple_basic(ocid))


    @FunLog()
    def test_save_ocid(self):
        urlString = f"https://open.api.nexon.com/maplestory/v1/id?character_name={self.character_name}"
        response = requests.get(urlString, headers = self.headers)
        try:
            if response.status_code == 200:
                ocid_dto = OcidDTO(
                    ocid = response.json()['ocid'],
                                 nickname = self.character_name)
                self.maple_service.save_ocid(ocid_dto)
            else:
                raise Exception(f"{response.json()['error']['name']}")
        except Exception as e:
            print(e)

    @FunLog()
    def test_save_maple_basic(self):
        ocid_str = self.maple_service.get_ocid(self.character_name).ocid
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
                maplebasic_dto = MapleBasicDTO(
                    level = level,
                    date = date,
                    guild_name = guild_name,
                    image = image,
                    unit_class = C_class,
                    union_lv = unionLv,
                    dojang = dojang,
                    ocid = ocid_str
                )
                self.maple_service.save_maple_basic(maplebasic_dto)
                print("maplebasic 삽입 완료")
        except Exception as e:
            print(e)
            return e
