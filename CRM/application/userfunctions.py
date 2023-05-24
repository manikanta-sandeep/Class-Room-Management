from .database import db
from .email import emailTo
from .local_time import *
from base64 import b64encode



class userfunctions:
    def send_mail_to(self,email,subject,msg):
        e=emailTo()
        e.send_email(subject,[email],msg)
        return 1

    def send_mail_to_list(self,email,subject,msg):
        e=emailTo()
        e.send_email(subject,email,msg)
        return 1

    def send_verification(self,email):
        e=emailTo()
        password=e.generate_password()
        msg=f'''
Hi ,

Thank you for registering your account on Project CRM. Hope you will find it easier to use. Here is the verification code, please verify your account with the below verification code.


{password}

Thanks and Regards
Manikanta Sandeep
Team Project CRMS.
        '''
        userfunctions().new_user(email,password)
        return userfunctions().send_mail_to(email,"Verification code for account creation",msg)
        
    def send_activation_verification(self,email,data):
        e=emailTo()
        password=e.generate_password()
        msg=f'''
Hi ,

We found your details in our database. Thank you for activation your account on Project CRM. Hope you will find it easier to use. Here is the verification code, please verify your account with the below verification code.

Your details:
GITAM Mail ID:  {data[0]}
GITAM ID     :  {data[1]}

Verification Code:  {password}

If you find any errors in the details, please reply to this mail with the same.

Thanks and Regards
Manikanta Sandeep
Team Project CRMS.
        '''
        userfunctions().new_user(email,password)
        return userfunctions().send_mail_to(email,"Verification code for account creation",msg)
        

    def forgot_send_verification(self,email):
        a=userfunctions().check_username(email)
        if a==-1:
            return -1
        else:
            e=emailTo()
            password=e.generate_password()
            msg=f'''
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body>
    <span style="font-family: Arial, Helvetica, sans-serif; font-size: 12px; color: #BBBBBB;">

Hi ,

You are recently requested for resetting your password for your account on Project CRM. Here is the verification code, please reset your account password with the below verification code.


{password}

Thanks and Regards
Manikanta Sandeep
Team Project CRMS.

    </span>
    </body>
</html>

        '''
            userfunctions().new_user(email,password)
            return userfunctions().send_mail_to(email,"Verification code for Reset Password",msg)
        
    def isalreadyuser(self,email):
        a=db.session.execute("select email,gid from user where email=:e and created_time is NULL",{"e":email})
        a=a.fetchall()
        print(a)
        if len(a)==1:
            return 1,a[0]
        else:
            return 0,[]
    
    
    def user_status(self,user_email):
        a=db.session.execute("select password from user where email=:mail",{"mail":user_email})
        no_of_users=a.fetchall()
        if len(no_of_users)==1:
            return 1
        return 0

    def current_availability(self,usid):
        t=time_calc().pcn()
        gid=db.session.execute('select gid from user where user_id=:uid',{"uid":usid})
        uid=gid.fetchall()
        #print(uid)
        uid=uid[0][0]
        #print(t,uid)
        prev=db.session.execute('select c.class_id,c.room_id,r.room_no,c.faculty_id,c.incharge_id,c.session_time, c.start_time,c.end_time,c.temporary,c.conflicted,c.remarks from classes c, rooms r where c.room_id=r.room_id and c.weekday=:wday and (c.st<=:pt and :pt<=c.et) and (c.faculty_id=:uid or c.incharge_id=:uid)',{"uid":uid,"pt":t[0][1],"wday":t[3]})
        p=prev.fetchall()
        cur=db.session.execute('select c.class_id,c.room_id,r.room_no,c.faculty_id,c.incharge_id,c.session_time, c.start_time,c.end_time,c.temporary,c.conflicted,c.remarks from classes c, rooms r where c.room_id=r.room_id and c.weekday=:wday and (c.st<=:pt and :pt<=c.et) and (c.faculty_id=:uid or c.incharge_id=:uid)',{"uid":uid,"pt":t[1][1],"wday":t[3]})
        c=cur.fetchall()
        nxt=db.session.execute('select c.class_id,c.room_id,r.room_no,c.faculty_id,c.incharge_id,c.session_time, c.start_time,c.end_time,c.temporary,c.conflicted,c.remarks from classes c, rooms r where c.room_id=r.room_id and c.weekday=:wday and (c.st<=:pt and :pt<=c.et) and (c.faculty_id=:uid or c.incharge_id=:uid)',{"uid":uid,"pt":t[2][1],"wday":t[3]})
        n=nxt.fetchall()
        data=(p,c,n)
        #print(data)
        return data,uid

    def isuser_registered(self,uid):
        a=db.session.execute('select email,gid,created_time from user where user_id=:uid',{"uid":uid})
        a=a.fetchall()[0]
        if a[2]!=None:
            return 1,[]
        else:
            return 0,a
    
    def user_id_withgid(self,gid):
        a=db.session.execute('select user_id from user where gid=:gid',{"gid":gid})
        a=a.fetchall()[0][0]
        return a

    def gid_withuid(self,uid):
        a=db.session.execute('select gid from user where user_id=:gid',{"gid":uid})
        a=a.fetchall()[0][0]
        return a

    def new_user(self,user_email,password):
        join_time=time_calc().time()
        already_present=db.session.execute("select count(*) from user where email=:mail",{"mail":user_email})
        if int(already_present.fetchall()[0][0])==0:
            db.session.execute("insert into user(email,password,created_time) values (:email,:pwd,:time)",{"email":user_email,"pwd":password, "time":join_time})
        else:
            db.session.execute("update user set password=:password where email=:mail",{"mail":user_email,"password":password})
        db.session.commit()
        return

    def check_user(self,user_email,password):
        a = db.session.execute("select password from user where email=:mail",{"mail": user_email})
        fetched_password = list(a.fetchall())
        print(fetched_password)
        #print(fetched_password,password,fetched_password==password)
        if len(fetched_password) != 0:
            f2=list(fetched_password[0])
            if f2[0]== password:
                return 1
            else:
                return 0
        else:
            return 0

    def join_user(self,email,name1,name,dob,password,profile_picture,gender,gid):
        join_time=time_calc().time()
        gender=int(gender)
        #profile_picture=b64encode(profile_picture).decode("utf-8")
        db.session.execute("update user set name=:n, dob=:dob, password=:pwd, profile_picture=:pp, gender=:g, created_time=:jt,gid=:gid where email=:mail",{ "mail":email ,"n":name,"pwd":password, "dob":dob, "pp":profile_picture, "g":gender ,"gid":gid, "jt":join_time})
        db.session.commit()
        return

    def fp_update_password(self,email,password):
        db.session.execute("update user set password=:pwd where email=:mail",{"mail":email,"pwd":password})
        db.session.commit()
        return

    def user_name(self,email):
        a=db.session.execute("select user_id,name from user where email=:mail",{"mail":email})
        u_id_name=list(a.fetchall())
        print(len(u_id_name),"Length")
        return u_id_name

    def account_details(self,user_id):
        a=db.session.execute("select u.user_id, u.email, u.name, u.dob, u.profile_picture, u.gender, u.created_time, u.last_update, u.gid, u.phone, u.profile_description from user u  where u.user_id=:uid",{"uid":user_id})
        details=list(a.fetchall())
        #print(len(details))
        if len(details)!=0:
            details=list(details[0])
            if details[4]=='' or details[4]=='None' or details[4]==None or details[4]=="b''" or str(details[4])=="b''":
                details[4]=-1
            else:
                details[4]=b64encode(details[4]).decode("utf-8")
            details[6]=time_calc().convert(details[6])
            return details
        
    def search_users(self,pattern,user_id):
        query='select email ,name ,profile_picture, gender, user_id from user where name like '+"'%"+pattern+"%'"
        a=db.session.execute(query)
        a=a.fetchall()
        l=[]
        for i in a:
            temp=list(i)
            if temp[2]=='' or temp[2]=='None' or temp[2]==None or temp[2]=="b''" or str(temp[2])=="b''":
                temp[2]=-1
            else:
                temp[2]=b64encode(temp[2]).decode("utf-8")
            l+=[temp]
        return l


    def add_userids(self):
        a=[['psingams@gitam.edu', 10175], ['amuddana@gitam.edu', 10117], ['sdevulap@gitam.edu', 700165], ['rvadali@gitam.edu', 10023], ['skadavil@gitam.edu', 600233], ['akatti@gitam.edu', 600472], ['dguha@gitam.edu', 600523], ['rsankara@gitam.edu', 600532], ['kmohamme@gitam.edu', 600548], ['dkunada@gitam.edu\n', 600553], ['rmalladi@gitam.edu', 600557], ['rsivaram@gitam.edu', 600572], ['svenduru@gitam.edu', 600578], ['rkypa@gitam.edu', 600582], ['nchittoj@gitam.edu', 600658], ['sravinut@gitam.edu', 12001], ['syedlapa@gitam.edu', 12002], ['nalvala@gitam.edu', 1918], ['sponnuru@gitam.edu', 10020], ['hgottumu@gitam.edu', 1340], ['sgudipat@gitam.edu', 10096], ['kmatti@gitam.edu', 10091], ['dsathamr@gitam.edu', 10094], ['jtirumal@gitam.edu', 10104], ['vpatloll@gitam.edu', 10129], ['aabdul@gitam.edu', 10130], ['rbabub@gitam.edu', 10133], ['jbankapa@gitam.edu', 10188], ['sdhaniko@gitam.edu', 10202], ['ygarapat@gitam.edu', 10204], ['atalluri@gitam.edu', 10215], ['pannabat@gitam.edu', 10217], ['psrisail@gitam.edu', 10222], ['kbatta@gitam.edu', 1349], ['rbhima@gitam.edu', 1944], ['rgurram@gitam.edu', 10230], ['rymd@gitam.edu', 10240], ['rmohd@gitam.edu', 10300], ['knidadav@gitam.edu', 10319], ['ashivamp@gitam.edu', 10325], ['msatti@gitam.edu', 1363], ['lkalahas@gitam.edu', 10366], ['vjoshi@gitam.edu', 10378], ['anitturu@gitam.edu', 10379], ['hkondamu@gitam.edu', 10381], ['vkommana@gitam.edu', 10386], ['kdumpal@gitam.edu', 10387], ['pbejjank@gitam.edu', 10390], ['ymaramre@gitam.edu', 10391], ['smekala@gitam.edu', 10395], ['lgiddalu@gitam.edu', 10396], ['mbolired@gitam.edu', 120015], ['vkanakal@gitam.edu', 600129], ['rkurilla@gitam.edu', 600290], ['rkarampu@gitam.edu', 600292], ['dvinod@gitam.edu', 600293], ['amohamma2@gitam.edu', 600294], ['rvannapu@gitam.edu', 600297], ['sguntaka@gitam.edu', 600300], ['byannam@gitam.edu', 600303], ['athakur@gitam.edu', 600305], ['nravula@gitam.edu', 600306], ['arajgopa@gitam.edu', 600307], ['ksharma@gitam.edu', 600344], ['pmundhe@gitam.edu', 600349], ['dbiradar@gitam.edu', 600363], ['panantul@gitam.edu', 600368], ['vsagenel@gitam.edu', 600394], ['kmuppava@gitam.edu', 600395], ['mgupta@gitam.edu', 600445], ['nchaudhu@gitam.edu', 600485], ['sgovatho@gitam.edu', 600489], ['sbera@gitam.edu', 600490], ['pbhagat@gitam.edu', 600492], ['kgidijal@gitam.edu', 120016], ['achwodap@gitam.edu', 600503], ['nmukku@gitam.edu', 600511], ['vdonthu@gitam.edu', 600513], ['mmula@gitam.edu', 600517], ['lgamidi@gitam.edu', 600535], ['pakkraba@gitam.edu', 600541], ['pyandrap@gitam.edu', 600542], ['bballa@gitam.edu', 600550], ['mdudekul@gitam.edu', 600566], ['jnaulega@gitam.edu', 600571], ['svedula3@gitam.edu', 600593], ['jgudeme@gitam.edu', 600617], ['jmedida@gitam.edu', 600629], ['nvarish@gitam.edu', 600631], ['mpatra2@gitam.edu', 600635], ['vkaturi@gitam.edu', 600657], ['kbommidi@gitam.edu', 600660], ['sjosyula@gitam.edu', 600667], ['jsharma@gitam.edu', 600668], ['ltalluri@gitam.edu', 600669], ['nkar@gitam.edu', 600679]]
        for i in a:
            db.session.execute('insert into user(email,gid) values(:c,:d)',{"c":i[0],"d":i[1]})
            db.session.commit()
        return


    def address_details(self,user_id):
        b=db.session.execute("select u.user_id,a.address, a.address2, a.phone, a.district, a.postal_code, c.city, s.state, cu.country from user u, address a, city c, state s, country cu where user_id=:uid and u.address_id=a.address_id and a.city_id=c.city_id and c.state_id=s.state_id and s.country_id=cu.country_id",{"uid":user_id})
        a=b.fetchall()
        a=list(a)
        print(a)
        if len(a)==0:
            #print(0)
            return 0
        else:
            print(1)
            return a[0]


    def follow_details(self,k,code):
        if k==0:
            user_id=userfunctions().get_uid_from_email(code)
        else:
            user_id=code
        following=db.session.execute("select count(*) from follows where follower_id=:id",{"id":user_id})
        followers=db.session.execute("select count(*) from follows where user_id=:id",{"id":user_id})
        posts=db.session.execute("select count(*) from blogs where user_id=:id",{"id":user_id})
        followers,following,posts=followers.fetchall()[0][0],following.fetchall()[0][0],posts.fetchall()[0][0]
        return [followers,following,posts]



    def delete_account(self,email):
        db.session.execute("delete from user where email=:mail",{"mail":email})
        db.session.commit()
        return

    def update_profile(self,email,n,dob,g,pp,m,pd,r):
        w=db.session.execute("select email,name,dob,gender,profile_picture,phone,phone, profile_description,role from user where email=:mail",{"mail":email})
        old_data=w.fetchall()[0]
        t=time_calc().time()
        if n!='':
            n1=n
        else:
            n1=old_data[1]
        if dob!='':
            dob1=dob
        else:
            dob1=old_data[2]
        if g!='':
            g1=g
        else:
            g1=old_data[3]
        #print(pp)
        if pp=="" or str(pp)=="b''" or str(pp)=='':
            pp1=old_data[4]
        else:
            pp1=pp
        
        if m!='':
            m1=m
        else:
            m1=old_data[6]
        if pd!='':
            pd1=pd
        else:
            pd1=old_data[7]
        if r!='':
            r1=r
        else:
            r1=old_data[8]
            
        #print(old_data[1:])
        #print(un,n,dob,g,pp)
        #print(un1,n1,dob1,g1,pp1)
        db.session.execute("update user set name=:n, dob=:dob, gender=:g, profile_picture=:pp,phone=:p,last_update=:l, profile_description=:pd, role=:r  where email=:mail",{"mail":email,"pd":pd1,"r":r1,"n":n1,"dob":dob1,"g":g1,"pp":pp1,"p":m1,"l":t})
        db.session.commit()
        return n1

    

    def check_username(self,email):
        a=db.session.execute("select name,password, user_id, email, gender,dpt_id,role from user where email=:mail",{"mail": email})
        a=list(a.fetchall())
        #print(a)
        if len(a)==0:
            return -1
        return list(a[0])

    def modify_account(self,email,name,dob,gender,pp):
        old=db.session.execute("select dob,profile_picture,user_id from user where email=:mail",{"mail":email})
        old=old.fetchall()[0]
        if dob=='-1':
            dob=old[0]
        if pp=="" or str(pp)=="b''":
            pp=old[1]
        db.session.execute("update user set name=:n, dob=:dob, gender=:g, profile_picture=:pp where user_id=:id",{"id":old[2],"n":name, "dob":dob,"g":gender, "pp":pp})
        db.session.commit()
        return old[2]


    def u_details(self,uid):
        d=db.session.execute("select u.email,u.name,u.dob,u.gender,u.profile_picture,u.aadhar,u.phone, u.profile_description,r.role_name from user u, roles r where u.role=r.role_id and user_id=:uid",{"uid":uid})    
        d=d.fetchall()[0]
        d=list(d)
        if d[4]=='' or d[4]=='None' or d[4]==None or d[4]=="b''" or str(d[4])=="b''":
            d[4]=-1
        else:
            d[4]=b64encode(d[4]).decode("utf-8")
        return d

    def u_details(self,uid):
        d=db.session.execute("select u.email,u.name,u.dob,u.gender,u.profile_picture,u.aadhar,u.phone, u.profile_description,r.role_name from user u, roles r where u.role=r.role_id and user_id=:uid",{"uid":uid})    
        d=d.fetchall()[0]
        d=list(d)
        if d[4]=='' or d[4]=='None' or d[4]==None or d[4]=="b''" or str(d[4])=="b''":
            d[4]=-1
        else:
            d[4]=b64encode(d[4]).decode("utf-8")
        return d

    def all_details(self,uid):
        d=db.session.execute("select u.email,u.name,u.dob,u.gender,u.profile_picture,u.aadhar,u.phone, u.profile_description,r.role_name from user u, roles r where u.role=r.role_id and user_id=:uid",{"uid":uid})    
        d=d.fetchall()[0]
        d=list(d)
        if d[4]=='' or d[4]=='None' or d[4]==None or d[4]=="b''" or str(d[4])=="b''":
            d[4]=-1
        else:
            d[4]=b64encode(d[4]).decode("utf-8")
        return d

    
    def get_username(self, uid):
        u=db.session.execute("select name from user where user_id=:uid",{"uid":uid})
        u=u.fetchall()
        u=u[0][0]
        #print(u)
        return u

    def get_userid(self):
        a=db.session.execute("select gid from user")
        a=a.fetchall()
        return a
