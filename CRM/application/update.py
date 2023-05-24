from .database import db 
from .local_time import *


class update:
    def insert_role(self,role_name):
        time=time_calc().time()
        try:
            #print(role_name, time)
            db.session.commit()
            db.session.execute("insert into roles(role_name, last_update) values (:n,:t) ",{"n":role_name,"t":time})
            db.session.commit()
        except:
            return 0
        return 1

    def insert_item_type(self,role_name):
        try:
            db.session.execute("insert into item_type(type_name) values (:n) ",{"n":role_name})
            db.session.commit()
        except:
            return 0
        return 1