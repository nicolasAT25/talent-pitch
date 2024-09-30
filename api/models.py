# from database import Base
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.ext.declarative import declarative_base
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    identification_number = Column(BigInteger, nullable=False)
    slug = Column(String, nullable=False)
    video = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    gender = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    
    
class Profile(Base):
    __tablename__ = "profiles"     # Name we want to give the table in postgres.
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    onboarding_goal = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True)
    views = Column(Integer, nullable=False)
    
    
class Challenge(Base):
    __tablename__ = "challenges"     # Name we want to give the table in postgres.
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)
    opencall_objective = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    
    
class Resume(Base):
    __tablename__ = "resumes"     # Name we want to give the table in postgres.
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    video = Column(String, nullable=False)
    views = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
   