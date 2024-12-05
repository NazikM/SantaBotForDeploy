import random

import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure database connection
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the santaBot table as a model
class SantaBot(Base):
    __tablename__ = "santaBot"
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False)
    name = Column(String, nullable=False)
    name_id = Column(String, nullable=False)
    organizer = Column(Boolean, nullable=False)
    wish_list = Column(Text)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Functions
def addToDB(group_name, name, name_id, organizer):
    db = next(get_db())
    new_entry = SantaBot(group_name=group_name, name=name, name_id=name_id, organizer=organizer)
    db.add(new_entry)
    db.commit()

def checkGroupExists(group_name):
    db = next(get_db())
    result = db.query(SantaBot).filter(SantaBot.group_name == group_name).first()
    return result is not None

def checkUserExists(name_id):
    db = next(get_db())
    result = db.query(SantaBot).filter(SantaBot.name_id == name_id).first()
    return result is not None

def checkUserExistsInGroup(name_id, group_name):
    db = next(get_db())
    result = db.query(SantaBot).filter(SantaBot.name_id == name_id, SantaBot.group_name == group_name).first()
    return result is not None

def checkOrganizerByUserID(name_id):
    db = next(get_db())
    result = db.query(SantaBot).filter(SantaBot.name_id == name_id, SantaBot.organizer.is_(True)).first()
    return result is not None

def getGroupNameByUserID(name_id):
    db = next(get_db())
    result = db.query(SantaBot.group_name).filter(SantaBot.name_id == name_id).first()
    return result.group_name if result else None

def getNamesByGroup(group_name):
    db = next(get_db())
    results = db.query(SantaBot.name).filter(SantaBot.group_name == group_name).all()
    return [name.name for name in results]

def getNameIdByName(name, group_name):
    db = next(get_db())
    result = db.query(SantaBot.name_id).filter(SantaBot.name == name, SantaBot.group_name == group_name).first()
    return result.name_id if result else None

def getOrganizerGroup(group_name):
    db = next(get_db())
    result = db.query(SantaBot.name_id).filter(SantaBot.group_name == group_name, SantaBot.organizer.is_(True)).first()
    return result.name_id if result else None

def addWishListByUserID(name_id, wish_list):
    db = next(get_db())
    db.query(SantaBot).filter(SantaBot.name_id == name_id).update({"wish_list": wish_list})
    db.commit()

def getWishListByName(name, group_name):
    db = next(get_db())
    result = db.query(SantaBot.wish_list).filter(SantaBot.name == name, SantaBot.group_name == group_name).first()
    if result and result.wish_list:
        return result.wish_list
    return "Я чекаю щось чудове, я тобі довіряю🤗"

def deleteRecordsByGroupName(group_name):
    db = next(get_db())
    db.query(SantaBot).filter(SantaBot.group_name == group_name).delete()
    db.commit()

def close_db():
    pass  # Not needed for SQLAlchemy as sessions are handled with `get_db()`
