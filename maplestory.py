import requests
from CustomException import apierror
from datetime import datetime, timedelta
from database import maplecon
from dotenv import load_dotenv
import os


class maplestoryC():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("nexonapi")
        self.headers = {
         "x-nxopen-api-key": self.api_key
        }
        self.maplecon = maplecon()

    def ocid(self,characterName):
        urlString = f"https://open.api.nexon.com/maplestory/v1/id?character_name={characterName}"
        response = requests.get(urlString, headers = self.headers)
        try:
            if response.status_code == 200:
                self.maplecon.insertMapleocid([response.json()['ocid'],characterName])
            else:
                raise apierror(f"{response.json()['error']['name']}")
        except apierror as e:
            return self.exceptname(e)

                
    def characterinfo(self,nickname):
        ocid = self.maplecon.findOcid(nickname)
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesteryesterday = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
        if self.update_time():
            basicUrlString = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date={yesterday}"
            unionUrlString = f"https://open.api.nexon.com/maplestory/v1/user/union?ocid={ocid}&date={yesterday}"
            dojangUrlString = f"https://open.api.nexon.com/maplestory/v1/character/dojang?ocid={ocid}&date={yesterday}"
        else:    
            basicUrlString = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date={yesteryesterday}"
            unionUrlString = f"https://open.api.nexon.com/maplestory/v1/user/union?ocid={ocid}&date={yesteryesterday}"
            dojangUrlString = f"https://open.api.nexon.com/maplestory/v1/character/dojang?ocid={ocid}&date={yesteryesterday}"
        try:
            responseBasic = requests.get(basicUrlString, headers = self.headers)
            responseUnion = requests.get(unionUrlString,headers= self.headers)
            responseDojang = requests.get(dojangUrlString,headers= self.headers)
            if responseBasic.status_code == 200 and responseUnion.status_code == 200 and responseDojang.status_code == 200:
                level = responseBasic.json()["character_level"]
                date = responseBasic.json()["date"]
                guildName = responseBasic.json()["character_guild_name"]
                image = responseBasic.json()["character_image"]
                C_class = responseBasic.json()["character_class"]
                unionLv = responseUnion.json()["union_level"]
                dojang = responseDojang.json()["dojang_best_floor"]
                self.maplecon.insertbasic(level,date,guildName,image,ocid,C_class,unionLv,dojang)
        except apierror as e:
            return self.exceptname(e)

    def updateCharacterinfo(self,nickname):
        ocid = self.maplecon.findOcid(nickname)
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        basicUrlString = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}&date={yesterday}"
        unionUrlString = f"https://open.api.nexon.com/maplestory/v1/user/union?ocid={ocid}&date={yesterday}"
        dojangUrlString = f"https://open.api.nexon.com/maplestory/v1/character/dojang?ocid={ocid}&date={yesterday}"
        try:
            responseBasic = requests.get(basicUrlString, headers = self.headers)
            responseUnion = requests.get(unionUrlString,headers= self.headers)
            responseDojang = requests.get(dojangUrlString,headers= self.headers)
            if responseBasic.status_code == 200 and responseUnion.status_code == 200 and responseDojang.status_code == 200:
                level = responseBasic.json()["character_level"]
                date = responseBasic.json()["date"]
                guildName = responseBasic.json()["character_guild_name"]
                image = responseBasic.json()["character_image"]
                C_class = responseBasic.json()["character_class"]
                unionLv = responseUnion.json()["union_level"]
                dojang = responseDojang.json()["dojang_best_floor"]
                self.maplecon.updateBasic(level,date,guildName,image,ocid,C_class,unionLv,dojang)
        except apierror as e:
            print("오류 발생")
            
    def update_time(self):
        today = datetime.today()
        if today.hour > 1 or (today.hour == 1 and today.minute >= 30):
            return True
        else:
            return False
    
    def exceptname(self,e):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        if e.message == "OPENAPI00005":
            print(f"[{formatted_time}]넥슨 API 키 오류, 개발자에게 문의하세요")
            return "넥슨 API 키 오류, 개발자에게 문의하세요"
        elif e.message == "OPENAPI00004":
            print(f"[{formatted_time}]캐릭터가 존재하지 않습니다., 장기 미접속 캐릭터인지 확인해 주세요")
            return "캐릭터가 존재하지 않습니다, 장기 미접속 캐릭터인지 확인해 주세요"
        else:
            print(f"[{formatted_time}]예외 오류!")
            print(e.message)
            return "오류 발생 개발자에게 문의하세요"