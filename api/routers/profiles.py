from fastapi import Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from .. import models, schemas, utils
from .. database import get_db, engine

from sqlalchemy.orm import Session
import os
import numpy as np
import pandas as pd
from typing import Annotated

router = APIRouter(
    prefix = "/profiles",
    tags = ["Profiles"]
    )

# Load batch data (max 3000 rows).
@router.post("/load_data")
def load_profiles(file:UploadFile=Annotated[bytes, File(...)]):        
    data = pd.read_csv(file.file, sep=",", encoding="utf-8")
    
    # Replce null values.
    if data.dtypes[data.dtypes == np.dtype("int64")].to_frame().reset_index(names="columns").__len__() > 0:
        for i in data.dtypes[data.dtypes == np.dtype("int64")].to_frame().reset_index(names="columns")["columns"]:
            data.fillna({i:0}, inplace=True)
    elif data.dtypes[data.dtypes == np.dtype("float64")].to_frame().reset_index(names="columns").__len__() > 0:
        for i in data.dtypes[data.dtypes == np.dtype("float64")].to_frame().reset_index(names="columns")["columns"]:
            data.fillna({i:0.0}, inplace=True)
    elif data.dtypes[data.dtypes == np.dtype("object")].to_frame().reset_index(names="columns").__len__() > 0:
        for i in data.dtypes[data.dtypes == np.dtype("object")].to_frame().reset_index(names="columns")["columns"]:
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