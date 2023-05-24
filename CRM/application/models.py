from application.database import db 
from sqlalchemy import ForeignKey,PrimaryKeyConstraint

class user(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String, unique=True)
    gid=db.Column(db.String,unique=True)
    name=db.Column(db.String)
    dob=db.Column(db.String)
    gender=db.Column(db.Integer)
    password=db.Column(db.String)
    phone=db.Column(db.Integer)
    profile_description=db.Column(db.String)
    profile_picture=db.Column(db.LargeBinary,default=None)
    created_time=db.Column(db.String)
    last_update=db.Column(db.String)
    role=db.Column(db.Integer)
    dpt_id=db.Column(db.Integer,ForeignKey("department.dpt_id"))

class timing(db.Model):
    __tablename__="timing"
    time_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    time=db.Column(db.Integer)


class classes(db.Model):
    __tablename__="classes"
    class_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id=db.Column(db.Integer)
    faculty_id=db.Column(db.Integer,ForeignKey("user.user_id"))
    created_by=db.Column(db.Integer, ForeignKey("user.user_id"))
    incharge_id=db.Column(db.Integer,default=0)
    session_time=db.Column(db.Integer,default=1)
    weekday=db.Column(db.Integer)
    start_time=db.Column(db.Integer)
    end_time=db.Column(db.Integer)
    cg_id=db.Column(db.Integer,ForeignKey("class_groups.cg_id"), default=None)
    st=db.Column(db.Integer)
    et=db.Column(db.Integer)
    temporary=db.Column(db.Integer,default=0)
    conflicted=db.Column(db.Integer,default=0)
    remarks=db.Column(db.String)
    created_time=db.Column(db.String)
    last_update=db.Column(db.String)



class rooms(db.Model):
    __tablename__="rooms"
    room_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_no=db.Column(db.String)
    dpt_id=db.Column(db.Integer)
    description=db.Column(db.String)
    date_joined=db.Column(db.String)

class department(db.Model):
    __tablename__="department"
    dpt_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    dpt_name=db.Column(db.String)
    dpt_hod=db.Column(db.Integer)
    description=db.Column(db.String)
    date_joined=db.Column(db.String)

class class_groups(db.Model):
    __tablename__="class_groups"
    cg_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    cg_name=db.Column(db.String)
    faculty_id=db.Column(db.Integer, ForeignKey("user.gid"))
    description=db.Column(db.String)
    email_ids=db.Column(db.String)
    joined_time=db.Column(db.String)
    last_update=db.Column(db.String)

class announcements(db.Model):
    __tablename__="announcements"
    ant_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    ant_subject=db.Column(db.String)
    group_id=db.Column(db.Integer, ForeignKey("class_groups.cg_id"))
    ant_message=db.Column(db.String)
    sent_time=db.Column(db.String)

class booking(db.Model):
    __tablename__="booking"
    booking_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_id=db.Column(db.Integer, ForeignKey("classes.class_id"))
    faculty_id=db.Column(db.Integer, ForeignKey("user.user_id"))
    reason=db.Column(db.String)
    joined_time=db.Column(db.String)
    last_update=db.Column(db.String)
