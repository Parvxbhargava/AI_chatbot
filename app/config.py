import os

class Config:
  SECRET_KEY=os.getenv("SECRET_KEY")
  SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL","sqlite:///db.sqlite3")
  SQLALCHEMY_TRACK_MODIFICATIONS=False
