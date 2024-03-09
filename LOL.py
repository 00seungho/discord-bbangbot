import requests
import time
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

class LOLAPI():
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("lolapi")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6,en-ZA;q=0.5",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.api_key
        }
    def getpuuid(self,arg):
        if(len(arg.split("#")) == 1):
            return "잘못된 닉네임입니다. 소환사 태그를 같이 입력해주세요.",-1
        nicknames = arg.split("#")
        nickname = nicknames[0]
        tag = nicknames[1]
        puidUrlString = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nickname}/{tag}"
        #puuid 얻어오는 구간
        puidResponse = requests.get(puidUrlString, headers = self.headers)
        if puidResponse.status_code == 200:
            puuid = puidResponse.json()["puuid"]
            return puuid,0
        else:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{formatted_time}] 소환사 조회 실패")
            return "소환사 조회에 실패했습니다. 닉네임을 확인해 주세요.",-1
    def getid(self,puuid):  
        idUrlString = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        #id 얻어오는 구간
        idResponse = requests.get(idUrlString, headers = self.headers)
        if idResponse.status_code == 200:
            return idResponse.json()["id"],0
        else:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{formatted_time}]by-puuid api 호출 오류")
            return "by-puuid api 호출 오류",-1

    async def get_info(self,args:tuple):
        start_time = time.time()
        summoner = args[0]
        championdata = args[1]
        
        #닉네임 얻기
        url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-puuid/{summoner['puuid']}"
        loop = asyncio.get_event_loop()    # 이벤트 루프 객체 얻기
        summonerNameResponse = await loop.run_in_executor(None, lambda: requests.get(url, headers=self.headers))
        if summonerNameResponse.status_code == 200:
            summonerNameResponse = summonerNameResponse.json()
        #티어 얻기
            url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner['summonerId']}"
            summonerTierResponse = await loop.run_in_executor(None, lambda: requests.get(url, headers=self.headers))
        if summonerTierResponse.status_code == 200:
            summonerTierResponse = summonerTierResponse.json()
            try:
                summoner["summonerName"] = f"{summonerNameResponse['gameName']}#{summonerNameResponse['tagLine']}"
            except Exception as e:
                pass
            try:
                summoner["SOLO_tier"] = "Unranked"
                summoner["SOLO_rank"] =""
                summoner["FREE_tier"] = "Unranked"
                summoner["FREE_rank"] = ""  
                for item in summonerTierResponse:
                    if item["queueType"] == "RANKED_SOLO_5x5":
                        summoner["SOLO_tier"] = item["tier"]
                        summoner["SOLO_rank"] = item["rank"]
                    elif item["queueType"] =="RANKED_FLEX_SR":
                        summoner["FREE_tier"] = item["tier"]
                        summoner["FREE_rank"] = item["rank"]
            except Exception as e:              
                pass    
        champion_id = int(summoner["championId"])
        champion = championdata[str(champion_id)]
        summoner["championname"] = champion
        return (summoner)
                
    async def ingameinfo(self,id):
            start_time = time.time()
            redteam = []
            blueteam = []
            championdata = {}
            ingameUrlString = f"https://kr.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{id}"
            #인게임 정보
            ingameUrlresponse = requests.get(ingameUrlString, headers = self.headers)
            if ingameUrlresponse.status_code == 200:
                url = "https://ddragon.leagueoflegends.com/cdn/14.2.1/data/ko_KR/champion.json"
                responseChampion= requests.get(url)
                if responseChampion.status_code == 200:
                    data = responseChampion.json()
                    data = data["data"]
                    for k,v in data.items():
                        championdata[v["key"]] = v["name"]
                    participants = ingameUrlresponse.json()["participants"]
                    summoners = await asyncio.gather(
                        self.get_info((participants[0], championdata)),
                        self.get_info((participants[1], championdata)),
                        self.get_info((participants[2], championdata)),
                        self.get_info((participants[3], championdata)),
                        self.get_info((participants[4], championdata)),
                        self.get_info((participants[5], championdata)),
                        self.get_info((participants[6], championdata)),
                        self.get_info((participants[7], championdata)),
                        self.get_info((participants[8], championdata)),
                        self.get_info((participants[9], championdata))
                    )
                    for summoner in summoners:
                        if summoner["teamId"] == 100:
                            redteam.append(summoner)
                        else:
                            blueteam.append(summoner)
                    end_time = time.time()
                    return (blueteam,redteam)
                else:
                    current_time = datetime.now()
                    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{formatted_time}]챔피언 목록 조회 실패, 관리자에게 물어보세요")
                    return(("챔피언 목록 조회 실패, 관리자에게 물어보세요"),-1)
            else:
                current_time = datetime.now()
                formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{formatted_time}]현재 게임중이 아닙니다.")
                return(("현재 게임중이 아닙니다."),-1)
