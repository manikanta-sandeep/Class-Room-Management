from .database import db
from .local_time import *
from base64 import b64encode
import re
from .userfunctions import *


class annfunctions:

    def email_preprocess(self,eid):
        eid=eid.split(",")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        temp=[]
        for i in eid:
            if(re.fullmatch(regex, i)):
                temp+=[i]
            else:
                print("invalid",i)
        print("Valid emails: ",temp)
        return temp

    def add_announcement(self,sub,cgid,msg):
        t=time_calc().time()
        db.session.execute('insert into announcements(ant_subject, group_id, ant_message, sent_time) values(:sub,:cgid,:msg,:t)',{"sub":sub,"cgid":cgid,"msg":msg,"t":t})
        db.session.commit()
        a=db.session.execute('select email_ids from class_groups where cg_id=:cgid',{"cgid":cgid})
        a=a.fetchall()
        if len(a)!=0:
            a=a[0][0]
            eids=annfunctions().email_preprocess(a)
            return userfunctions().send_mail_to_list(eids,sub,msg)
        return

    def get_anndetails(self,cgid):
        a=db.session.execute('select * from announcements where group_id=:cgid order by ant_id DESC',{"cgid":cgid})
        a=a.fetchall()
        return a
        

    