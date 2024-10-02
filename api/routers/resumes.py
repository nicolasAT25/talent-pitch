from fastapi import Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from .. import models, schemas
from .. database import get_db, engine

from sqlalchemy.orm import Session
import numpy as np
import pandas as pd
from typing import Annotated, List

router = APIRouter(
    prefix = "/resumes",
    tags = ["Resumes"]
    )

# Load batch data (max 3000 rows).
@router.post("/load_data")
def load_resumes(file:UploadFile=Annotated[bytes, File(...)]):
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
    data.to_sql(name="resumes", con=engine, if_exists="append", chunksize=3000, index=False)
    return Response(status_code=status.HTTP_200_OK)

# Get all resumes.
@router.get("/", response_model=List[schemas.Resume])
def get_resumes(db: Session=Depends(get_db)):
    resumes = db.query(models.Resume).all()
    return resumes

# Get one user by id.
@router.get("/{id}", response_model=schemas.Resume)
def get_resume(id:int, db: Session=Depends(get_db)):
    resume = db.query(models.Resume).filter(models.Resume.id == id).first()
    
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Resume with ID {id} does not exist")
               
    return resume

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Resume)
def create_resume(resume: schemas.ResumeCreate, db: Session=Depends(get_db)):
    new_resume = models.Resume(**resume.model_dump())   
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    return resume

# Delete a user.
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(id:int, db: Session=Depends(get_db)):
    resume_query = db.query(models.Resume).filter(models.Resume.id == id)
    resume_to_delete = resume_query.first()
    
    if not resume_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Resume with ID {id} does not exist")
        
    resume_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
