import requests
import dotenv
from dotenv import load_dotenv
import os
class imgEngine():
    
    def __init__(self) -> None:
        load_dotenv()
        self.api_key = os.getenv("kakaoapi")
        self.url = "https://dapi.kakao.com/v2/search/image"
        self.header = {'Authorization': self.api_key}
    def searching(self,query):
        queryString = {'query' : query}
        response = requests.get(self.url,headers=self.header,params=queryString)
        return response.json()["documents"][0]["image_url"]


