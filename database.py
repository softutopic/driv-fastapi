from sqlalchemy import create_engine
from config import settings

class Database:
    def __init__(self):
        self.engine = create_engine(
            f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
        )

    def get_connection(self):
        return self.engine.connect()

database = Database()