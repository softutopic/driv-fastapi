import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        db_username = os.getenv("DATABASE_USERNAME")
        db_password = os.getenv("DATABASE_PASSWORD")
        db_hostname = os.getenv("DATABASE_HOSTNAME")
        db_port = os.getenv("DATABASE_PORT")
        db_name = os.getenv("DATABASE_NAME")

        self.engine = create_engine(
            f"postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}", echo=True)

    def get_connection(self):
        return self.engine.connect()

database = Database()