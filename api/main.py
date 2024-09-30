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
        
############################## USERS ##############################

# # Load batch data (max 3000 rows).
# @round.post("/users/{file_name}")
# def load_users(file_name:str, col_to_hash: str, db: Session=Depends(get_db)):
#     separator = separator_finder(os.path.join(parent_path, file_name))
#     separator_finder
    
#     data = pd.read_csv(filepath_or_buffer=os.path.join(parent_path, file_name), sep=separator, encoding="utf-8")
    
#     # Replce null values.
#     if data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0.0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:"NA"}, inplace=True)
    
#     for col in col_to_hash.split(","):
#         data[col] = data[col].astype(str).apply(hash)
        

#     # Load data to postgres (new DB)
#     data.to_sql(name="users", con=engine, if_exists="replace", chunksize=3000, index=False, dtype={"created_at":TIMESTAMP, "updated_at":TIMESTAMP})
#     return Response(status_code=status.HTTP_200_OK)

# # Get all users.
# @router.get("/users")
# def get_users():
#     cursor.execute(""" SELECT * FROM users""")
#     users = cursor.fetchall()
#     return users

# # Get one user by id.
# @router.get("/users/{id}")
# def get_user(id:int):
#     cursor.execute(f""" SELECT * FROM users WHERE id = %s""", (id,))
#     users = cursor.fetchone()
#     return users

# # Create one user.
# @router.post("/users", status_code=status.HTTP_201_CREATED)
# def create_user():
#     cursor.execute("""
#                     INSERT INTO users (id,name,identification_number,slug,video,email,gender,created_at,updated_at)
#                     VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
#                     """, ("4000","Nicolás","1234567890","nico-at",None,"nico@test.com","M",datetime.now(),None)
#                     )

#     conn.commit()
#     return "User created."

# ############################## PROFILES ##############################

# # Load batch data (max 3000 rows).
# @app.post("/profiles/{file_name}")
# def load_profiles(file_name:str):
#     separator = separator_finder(os.path.join(parent_path, file_name))
#     separator_finder
    
#     data = pd.read_csv(filepath_or_buffer=os.path.join(parent_path, file_name), sep=separator, encoding="utf-8")
    
#     # Replce null values.
#     if data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0.0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:"NA"}, inplace=True)
        

#     # Load data to postgres (new DB)
#     data.to_sql(name="profiles", con=engine, if_exists="replace", chunksize=3000, index=False, dtype={"created_at":TIMESTAMP, "updated_at":TIMESTAMP})
#     return Response(status_code=status.HTTP_200_OK)

# # Get all profiles.
# @app.get("/profiles")
# def get_profiles():
#     cursor.execute(""" SELECT * FROM profiles""")
#     profiles = cursor.fetchall()
#     return profiles

# # Get one profile by id.
# @app.get("/profiles/{id}")
# def get_profile(id:int):
#     cursor.execute(f""" SELECT * FROM profiles WHERE id = %s""", (id,))
#     profiles = cursor.fetchone()
#     return profiles

# # Create one profile
# @app.post("/profiles", status_code=status.HTTP_201_CREATED)
# def create_profile():
#     cursor.execute("""
#                     INSERT INTO profiles (id,user_id,onboarding_goal,created_at,updated_at,views)
#                     VALUES (%s,%s,%s,%s,%s,%s);
#                     """, ("360","4000","be_discovered-[hire]",datetime.now(),None,10)
#                     )

#     conn.commit()
#     return "Profile created."


# ############################## RESUMES ##############################

# # Load batch data (max 3000 rows).
# @app.post("/resumes/{file_name}")
# def load_resumes(file_name:str):
#     separator = separator_finder(os.path.join(parent_path, file_name))
#     separator_finder
    
#     data = pd.read_csv(filepath_or_buffer=os.path.join(parent_path, file_name), sep=separator, encoding="utf-8")
    
#     # Replce null values.
#     if data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0.0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:"NA"}, inplace=True)
        

#     # Load data to postgres (new DB)
#     data.to_sql(name="resumes", con=engine, if_exists="replace", chunksize=3000, index=False, dtype={"created_at":TIMESTAMP, "updated_at":TIMESTAMP})
#     return Response(status_code=status.HTTP_200_OK)

# # Get all resumes.
# @app.get("/resumes")
# def get_resumes():
#     cursor.execute(""" SELECT * FROM resumes""")
#     resumes = cursor.fetchall()
#     return resumes

# # Get one user by id.
# @app.get("/resumes/{id}")
# def get_resume(id:int):
#     cursor.execute(f""" SELECT * FROM resumes WHERE id = %s""", (id,))
#     resumes = cursor.fetchone()
#     return resumes

# @app.post("/resumes", status_code=status.HTTP_201_CREATED)
# def create_resume():
#     cursor.execute("""
#                     INSERT INTO resumes (id,user_id,name,type,video,views,created_at)
#                     VALUES (%s,%s,%s,%s,%s,%s,%s);
#                     """, ("13","4000","Mi primer video","pitch_video",None,25,datetime.now())
#                     )

#     conn.commit()
#     return "Resume created."

# # Delete a user.
# @app.delete("/resumes/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_resume(id:int):
#     cursor.execute(f""" DELETE * FROM resumes WHERE id = %s""", (id,))
#     conn.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# ############################## CHALLENGES ##############################

# # Load batch data (max 3000 rows).
# @app.post("/challenges/{file_name}")
# def load_challenges(file_name:str):
#     separator = separator_finder(os.path.join(parent_path, file_name))
#     separator_finder
    
#     data = pd.read_csv(filepath_or_buffer=os.path.join(parent_path, file_name), sep=separator, encoding="utf-8")
#     data["created_at"] = pd.to_datetime(data["created_at"], format="%d/%m/%y")
    
#     # Replce null values.
#     if data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:0.0}, inplace=True)
#     elif data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns").__len__() > 0:
#         for i in data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns")["columns"]:
#             data.fillna({i:"NA"}, inplace=True)
        

#     # Load data to postgres (new DB)
#     data.to_sql(name="challenges", con=engine, if_exists="replace", chunksize=3000, index=False, dtype={"created_at":TIMESTAMP, "updated_at":TIMESTAMP})
#     return Response(status_code=status.HTTP_200_OK)

# # Get all challenges.
# @app.get("/challenges")
# def get_challenges():
#     cursor.execute(""" SELECT * FROM challenges""")
#     challenges = cursor.fetchall()
#     return challenges

# # Get one user by id.
# @app.get("/challenges/{id}")
# def get_challenge(id:int):
#     cursor.execute(f""" SELECT * FROM challenges WHERE id = %s""", (id,))
#     challenges = cursor.fetchone()
#     return challenges

# @app.post("/challenges", status_code=status.HTTP_201_CREATED)
# def create_resume():
#     cursor.execute("""
#                     INSERT INTO challenges (id,name,description,status,opencall_objective,created_at)
#                     VALUES (%s,%s,%s,%s,%s,%s);
#                     """, ("570","Nuevo desafío!!!","En busca de nuevo talento.","open","Artistas",datetime.now())
#                     )

#     conn.commit()
#     return "Challenge created."