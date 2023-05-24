from .database import db
from .local_time import *



class roomfunctions:
    def insert_rooms(self):
        '''a=['A-616',
            'A-421',
            'A-417',
            'A-614',
            'B-407',
            'B-406',
            'B-506',
            'A-613',
            'B-713',
            'A-317',
            'B-403',
            'B-504',
            'A-621',
            'A-321',
            'B-408',
            'A-615',
            'B-405',
            'B-503',
            'B-404',
            'B-507',
            'B-714',
            'A-617']'''
        a=['B-614']
        for i in a:
            t=time_calc().time()
            db.session.execute("insert into rooms(room_no, dpt_id,date_joined) values(:i,1,:t)",{"i":i,"t":t})
            db.session.commit()
        return

    def all_rooms(self):
        a=db.session.execute("select room_id,room_no from rooms")
        a=a.fetchall()
        return a  

    def all_dpts(self):
        a=db.session.execute("select dpt_id,dpt_name from department")
        a=a.fetchall()
        return a  

    def add_dpts(self):
        a=['CSE','MECH','ECE','CIVL','BSC']
        b=['Computer Science and Engineering','Mechanical Engineering','Electrical and Communications Engineering','Civil Engineering','Bachelor of Science']
        for i in range(len(a)):
            t=time_calc().time()
            db.session.execute("insert into department(dpt_name,dpt_hod,description,date_joined) values (:n,:h,:d,:t)",{"n":a[i],"h":1,"d":b[i],"t":t})
            db.session.commit()
        return