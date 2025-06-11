from app.extensions import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin,db.Model):
  id=db.Column(db.Integer,primary_key=True)
  email=db.Column(db.String(150),unique=True,nullable=False)
  password=db.Column(db.String(150),nullable=False)
  memories=db.relationship('LongTermMemory',backref='user',lazy=True)

class LongTermMemory(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  content=db.Column(db.String(1000),nullable=False)
  timestamp=db.Column(db.DateTime(timezone=True),default=func.now())

  user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
