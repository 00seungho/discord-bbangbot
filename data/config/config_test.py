import os

class TestDataBaseConfig():
    __test__ = False  # pytest가 테스트 클래스로 인식하지 않음
    host = os.getenv("test_host")
    user = os.getenv("test_user")
    password = os.getenv("test_password")
    db = os.getenv("test_db")
    port = os.getenv("port", "3306")  
    DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
