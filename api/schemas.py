from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from datetime import datetime


################# USERS #################
# Data recieved from the user
class UserCreate(BaseModel):
    name: str
    identification_number: str
    slug: str
    video: str
    email: EmailStr
    gender: str
    created_at: Optional[str] = datetime.now()       

# Data sent to the user
class User(BaseModel): 
    # id: int
    name: str
    email: EmailStr
    video: str
    created_at: datetime

    class Config:
        from_attributes = True 
        
################# PROFILES #################
# Data recieved from the user
class ProfileCreate(BaseModel):
    user_id: int
    onboarding_goal: str
    views: int                

# Data sent to the user
class Profile(ProfileCreate): 
    pass

    class Config:
        from_attributes = True 
        
################# RESUMES #################
# Data recieved from the user
class ResumeCreate(BaseModel):
    user_id: int
    name: str
    type: str
    video: str
    views: int              

# Data sent to the user
class Resume(ResumeCreate): 
    pass

    class Config:
        from_attributes = True 
        
################# CHALLENGES #################
# Data recieved from the user
class ChallegeCreate(BaseModel):
    name: str
    description: str
    status: str
    opencall_objective: str      

# Data sent to the user
class Challenge(ChallegeCreate): 
    pass

    class Config:
        from_attributes = True 