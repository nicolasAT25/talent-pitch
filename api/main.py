from fastapi import FastAPI
from .config import settings
from . import models
from .routers import users, profiles, resumes, challenges
from .database import engine

import psycopg2
from psycopg2.extras import RealDictCursor
import time


"""
Script to populate the new DB (source). In this case, data comes from a local file due to the
simplicity of the files used. However, the source could be another DB or any kind of source/repository.
"""

models.Base.metadata.create_all(bind=engine)    # Creates all models in the DB.

app = FastAPI()

app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(resumes.router)
app.include_router(challenges.router)

while True:
    try:
        # Usage of EV for security.
        conn = psycopg2.connect(host=settings.database_hostname, dbname=settings.database_name, user=settings.database_username, password=settings.database_password, 
                               cursor_factory=RealDictCursor)  # Map the columns and values
        cursor = conn.cursor()
        print('Database connection was succesfull!')
        break
    except Exception as e:
        print(f'Connecting to database failed. Error: {e}')
        time.sleep(2)