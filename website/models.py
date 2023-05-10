from calendar import c
from email.policy import default
from xmlrpc.client import Boolean
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# model for User registration
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    secondname = db.Column(db.String(150))
    idn = db.Column(db.Integer, nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)
    registerdate = db.Column(db.DateTime(timezone=True), default=func.now())
    password = db.Column(db.String(150))
    startdate = db.Column(db.DateTime(timezone=True), default=func.now())
    # procedure_id = db.Column(db.Integer)
    crop_id =db.Column(db.Integer)
    is_scheduled = db.Column(db.Boolean, default = False)
    country = db.Column(db.String(150), nullable=True)
    village = db.Column(db.String(150), nullable=True)
    sizeofland = db.Column(db.String(150), nullable=True)


class Procedure(db.Model):
    __tablename__ = "procedure"
    id = db.Column(db.Integer, primary_key=True)
    maintitle = db.Column(db.String(150))
    description = db.Column(db.String(150))
    weeks = db.relationship("Weeks")
    
    
class Weeks(db.Model):
    __tablename__ = "week"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    procedure_id = db.Column(db.Integer, db.ForeignKey("procedure.id"))
    activities = db.relationship("Activity")

class Activity(db.Model):
    __tablename__ = "activity"
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(1000))
    week_id = db.Column(db.Integer, db.ForeignKey("week.id"))
