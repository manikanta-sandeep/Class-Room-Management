from .database import db


class rolefunctions:
    def allroles(self):
        a=db.session.execute("select role_name from roles")
        a=a.fetchall()
        p=''
        for i in a:
            p+=str(i[0])+', '
        #print(p[:-2])
        return p[:-2]

    def delete_role(self, d_id):
        db.session.execute("delete from roles where role_id=:did",{"did":d_id})
        db.session.commit()
        return

    