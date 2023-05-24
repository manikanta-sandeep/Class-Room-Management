from .database import db 
from .local_time import *

from .userfunctions import *


class groupsfunctions:
    def addgroup(self,gname,fid,d,emi):
        t=time_calc().time()
        fid=userfunctions().gid_withuid(int(fid))
        db.session.execute('insert into class_groups(cg_name,faculty_id,description,email_ids,joined_time,last_update) values(:cn,:fid,:d,:emi,:t,:t)',{"cn":gname,"fid":fid,"d":d,"t":t,"emi":emi})
        db.session.commit()
        return 

    def all_groups(self,uid):
        uid=userfunctions().gid_withuid(int(uid))
        a=db.session.execute("select * from class_groups where faculty_id=:fid",{"fid":uid})
        a=a.fetchall()
        return a

    def get_all_cgdata(self,cgid):
        a=db.session.execute("select cg.cg_id,cg.cg_name,cg.faculty_id,cg.description,cg.email_ids,cg.joined_time,cg.last_update,u.name from class_groups cg, user u where cg_id=:cgid and u.gid=cg.faculty_id",{"cgid":cgid})
        a=a.fetchall()
        return a

    def remove_class_group(self,cgid):
        db.session.execute('delete from class_groups where cg_id=:cgid',{"cgid":cgid})
        db.session.commit()
        return

    def get_cgdata(self,cgid):
        a=db.session.execute("select cg_name,email_ids,description,cg_id from class_groups where cg_id=:cgid",{"cgid":cgid})
        a=a.fetchall()
        return a[0]

    def all_cg_list(self,uid):
        uid=userfunctions().gid_withuid(int(uid))
        a=db.session.execute("select cg_id,cg_name from class_groups where faculty_id=:fid",{"fid":uid})
        a=a.fetchall()
        return a

    def update_classg(self,cg_id,cgn,d,emi):
        t=time_calc().time()
        a=db.session.execute("select * from class_groups where cg_id=:cid",{"cid":cg_id})
        a=a.fetchall()[0]
        if cgn!='':
            cgn1=cgn
        else:
            cgn1=a[1]
        if d!='':
            d1=d
        else:
            d1=a[3]
        if emi!='':
            emi1=emi
        else:
            emi1=a[4]
        db.session.execute('update class_groups set cg_name=:cgn, description=:d, email_ids=:emi, last_update=:t where cg_id=:cgid',{"cgn":cgn1,"d":d1,"emi":emi1,"t":t,"cgid":cg_id})
        db.session.commit()
        return

            
            