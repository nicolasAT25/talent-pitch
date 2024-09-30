from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db, engine

from sqlalchemy.orm import Session
import os
import pandas as pd

router = APIRouter(
    prefix = "/users",  # Avoid to indicate the path operation root
    tags = ["Users"]    # Create section in Swagger documentation
    )

# Define local paths.
parent_path = r"/Users/nicolasarangurenturmeque/Documents/TalentPitchAPI/api/data/"

# Load batch data (max 3000 rows).
@router.post("/{file_name}")
def load_users(file_name:str, cols_to_hash:str):
    separator = utils.separator_finder(os.path.join(parent_path, file_name))
    
    data = pd.read_csv(filepath_or_buffer=os.path.join(parent_path, file_name), sep=separator, encoding="utf-8")
    
    # Replce null values.
    if data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns").__len__() > 0:
        for i in data.dtypes[data.dtypes == 'int64'].to_frame().reset_index(names="columns")["columns"]:
            data.fillna({i:0}, inplace=True)
    elif data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns").__len__() > 0:
        for i in data.dtypes[data.dtypes == 'float64'].to_frame().reset_index(names="columns")["columns"]:
            data.fillna({i:0.0}, inplace=True)
    elif data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns").__len__() > 0:
        for i in data.dtypes[data.dtypes == 'object'].to_frame().reset_index(names="columns")["columns"]:
            data.fillna({i:"NA"}, inplace=True)
    
    for col in cols_to_hash.split(","):
        data[col] = data[col].astype(str).apply(hash)
        
    # Load data to postgres (new DB)
    data.to_sql(name="users", con=engine, if_exists="append", chunksize=3000, index=False)
    return Response(status_code=status.HTTP_200_OK)

# Get all users.
@router.get("/")
def get_users(db: Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Get one user by id.
@router.get("/{id}")
def get_user(id:int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID {id} does not exist")
    return user

# Create one user.
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    hashed_password = utils.hash(user.identification_number)
    user.identification_number = hashed_password
    new_user = models.User(**user.model_dump())   
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db: Session = Depends(get_db)):    
    user_query = db.query(models.User).filter(models.User.id == id)
    user_to_delete = user_query.first()
    
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID {id} does not exist")
        
    user_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)