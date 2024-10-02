from fastapi import Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from .. import models, schemas
from .. database import get_db, engine

from sqlalchemy.orm import Session
import numpy as np
import pandas as pd
from typing import Annotated, List

router = APIRouter(
    prefix = "/challenges",
    tags = ["Challenges"]
    )

# Load batch data (max 3000 rows).
@router.post("/load_data}")
def load_challenges(file:UploadFile=Annotated[bytes, File(...)]):
        
    data = pd.read_csv(file.file, sep=";", encoding="utf-8")
    data["created_at"] = pd.to_datetime(data["created_at"], format="%d/%m/%y")
    
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
    data.to_sql(name="challenges", con=engine, if_exists="append", chunksize=3000, index=False)
    return Response(status_code=status.HTTP_200_OK)

# Get all challenges.
@router.get("/", response_model=List[schemas.Challenge])
def get_challenges(db: Session=Depends(get_db)):
    challenge = db.query(models.Challenge).all()
    return challenge

# Get one user by id.
@router.get("/{id}", response_model=schemas.Challenge)
def get_challenge(id:int, db: Session=Depends(get_db)):
    challenges = db.query(models.Challenge).filter(models.Challenge.id == id).first()
    
    if not challenges:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Challenge with ID {id} does not exist")
    return challenges

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Challenge)
def create_resume(challenge: schemas.ChallegeCreate, db: Session=Depends(get_db)):
    new_challenge = models.Challenge(**challenge.model_dump())   
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    return challenge

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_challenge(id:int, db: Session = Depends(get_db)):    
    challenge_query = db.query(models.Challenge).filter(models.Challenge.id == id)
    challenge_to_delete = challenge_query.first()
    
    if not challenge_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Challenge with ID {id} does not exist")
        
    challenge_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)