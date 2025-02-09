import requests
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from data.dto import MapleBasicDTO, OcidDTO

class MaplestoryAPI():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("nexonapi")
        self.headers = {
         "x-nxopen-api-key": self.api_key
        }

    def get_nexon_to_ocid(self,characterName) -> OcidDTO:
        """
        캐릭터의 이름을 받아 넥슨 api에서 ocid를 조회하는 함수
        return: OcidDTO
        Error return: None
        """
        urlString = f"https://open.api.nexon.com/maplestory/v1/id?character_name={characterName}"
        response = requests.get(urlString, headers = self.headers)
        if response.status_code == 200:
            ocid_dto = OcidDTO(nickname=characterName, ocid=response.json()['ocid'])
            return ocid_dto
        else:
            return None

    def get_nexon_maplebasic(self,ocid:str):
        now = datetime.now(timezone(timedelta(hours=9)))
        update_time = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone(timedelta(hours=9)))
        if now >= update_time:
            update_date = (now - timedelta(days=2)).strftime("%Y-%m-%d")
        else:
            update_date = (now - timedelta(days=3)).strftime("%Y-%m-%d")

        basicUrlString = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date={update_date}"
        unionUrlString = f"https://open.api.nexon.com/maplestory/v1/user/union?ocid={ocid}&date={update_date}"
        dojangUrlString = f"https://open.api.nexon.com/maplestory/v1/character/dojang?ocid={ocid}&date={update_date}"
        responseBasic = requests.get(basicUrlString, headers = self.headers)
        responseUnion = requests.get(unionUrlString,headers= self.headers)
        responseDojang = requests.get(dojangUrlString,headers= self.headers)
        if responseBasic.status_code == 200 and responseUnion.status_code == 200 and responseDojang.status_code == 200:
            level = responseBasic.json()["character_level"]
            date = responseBasic.json()["date"]
            guild_name = responseBasic.json()["character_guild_name"]
            image = responseBasic.json()["character_image"]
            unit_class = responseBasic.json()["character_class"]
            union_lv = responseUnion.json()["union_level"]
            dojang = responseDojang.json()["dojang_best_floor"]
            maple_basic_dto = MapleBasicDTO(
                ocid=ocid,
                level=level,
                date=date,
                image=image,
                guild_name=guild_name,
                unit_class=unit_class,
                union_lv=union_lv,
                dojang=dojang
            )
            return maple_basic_dto
        else:
            print(responseBasic.status_code)
            print(responseDojang.status_code)
            print(responseUnion.status_code)
            return None
            
    def is_latest_update(self,db_date: datetime) -> bool:
        now = datetime.now() + timedelta(hours=9)  # UTC+9 (KST)
        yesterday = (now - timedelta(days=1)).date()
        update_yesterday = db_date.date() == yesterday
        return update_yesterday and now >= db_date
    
