import os
from dotenv import load_dotenv
load_dotenv()

# Set environment variables
class Settings(object):
    database_hostname=os.environ.get("DATABASE_HOST_NAME")
    database_port=os.environ.get("DATABASE_PORT")
    database_password=os.environ.get("DATABASE_PASSWORD")
    database_name=os.environ.get("DATABASE_NAME")
    database_username=os.environ.get("DATABASE_USERNAME")

    class Config:
        env_file = '.env'

settings = Settings()