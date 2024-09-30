from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db, engine
from ..utils import separator_finder

from sqlalchemy.orm import Session
from sqlalchemy import TIMESTAMP
import os
import pandas as pd
from datetime import datetime

router = APIRouter(
    prefix = "/profiles",  # Avoid to indicate the path operation root
    tags = ["Profiles"]    # Create section in Swagger documentation
    )

# Define local paths.
parent_path = r"/Users/nicolasarangurenturmeque/Documents/TalentPitchAPI/api/data/"

# Load batch data (max 3000 rows).
@router.post("/{file_name}")
def load_profiles(file_name:str):
    separator = separator_finder(os.path.join(parent_path, file_name))
        
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
        
    # Load data to postgres (new DB)
    data.to_sql(name="profiles", con=engine, if_exists="append", chunksize=3000, index=False)
    return Response(status_code=status.HTTP_200_OK)

# Get all profiles.
@router.get("/")
def get_profiles(db: Session=Depends(get_db)):
    profiles = db.query(models.Profile).all()
    return profiles

# Get one profile by id.
@router.get("/{id}")
def get_profile(id:int, db: Session=Depends(get_db)):
    profile = db.query(models.Profile).filter(models.Profile.id == id).first()
    
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with ID {id} does not exist")
    return profile

# Create one profile
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_profile(profile:schemas.ProfileCreate, db: Session=Depends(get_db)):
    new_profile = models.Profile(**profile.model_dump())
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return profile

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(id:int, db: Session = Depends(get_db)):    
    profile_query = db.query(models.Profile).filter(models.Profile.id == id)   
    profile_to_delete = profile_query.first()
    
    if not profile_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Profile with ID {id} does not exist")
        
    profile_query.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)