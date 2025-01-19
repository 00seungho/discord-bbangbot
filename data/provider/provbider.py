from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.config import DataBaseConfig
from data.config import TestDataBaseConfig
import os
from dotenv import load_dotenv
from data.entity.base import Base

class SessionProvider:
    def __init__(self):
        load_dotenv()
        self.env = os.getenv("ENV", "production")
        if self.env == "test":
            print("This module is running in a test environment")
            print(TestDataBaseConfig.DATABASE_URL)
            self.engine = create_engine(TestDataBaseConfig.DATABASE_URL, echo=True)
            Base.metadata.create_all(self.engine)
            self.SessionFactory = sessionmaker(bind=self.engine)
        else:
            self.engine = create_engine(DataBaseConfig.DATABASE_URL, echo=True)
            self.SessionFactory = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.SessionFactory()
