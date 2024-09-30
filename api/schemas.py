from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from datetime import datetime


################# USERS #################
# Data recieved from the user
class UserBase(BaseModel):
    id: Optional[int]
    name: str
    identification_number: str
    slug: str
    video: str
    email: EmailStr
    gender: str
    

class UserCreate(UserBase):
    pass                

# Data sent to the user
class User(BaseModel): 
    id: int
    name: str
    video: str
    reated_at: datetime

    class Config:
        from_attributes = True 
        
################# PROFILES #################
# Data recieved from the user
class ProfileBase(BaseModel):
    id: Optional[int]
    user_id: int
    onboarding_goal: str
    views: int

class ProfileCreate(ProfileBase):
    pass                

# Data sent to the user
class Profile(ProfileCreate): 
    pass

    class Config:
        from_attributes = True 
        
################# RESUMES #################
# Data recieved from the user
class ResumeBase(BaseModel):
    id: Optional[int]
    user_id: int
    name: str
    type: str
    video: str
    views: int

class ResumeCreate(ResumeBase):
    pass                

# Data sent to the user
class Resume(ResumeCreate): 
    created_at: datetime

    class Config:
        from_attributes = True 
        
################# CHALLENGES #################
# Data recieved from the user
class ChallegeBase(BaseModel):
    # id: Optional[int]
    name: str
    description: str
    status: str
    opencall_objective: str

class ChallegeCreate(ChallegeBase):
    pass                

# Data sent to the user
class Challege(ChallegeCreate): 
    pass

    class Config:
        from_attributes = True 