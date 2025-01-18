from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
db = os.getenv("db")
port = os.getenv("port", "3306")  
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(DATABASE_URL, echo=True)
SessionFactory = sessionmaker(bind=engine)