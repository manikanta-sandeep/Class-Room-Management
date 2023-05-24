from flask import render_template, redirect, request, session
from flask import current_app as app
from .database import db 

from .userfunctions import *
from .clocation import *
from .analysis import *
from .room_functions import *
from .class_functions import *
from .email import *
from .classgroup_functions import *

@app.route("/", methods=["GET","POST"])
def index_page():
    db.session.execute("select * from user")
    if request.method=="GET":
        return render_template("index_page.html")
    else:
        return render_template("index_page.html")


@app.route("/login",methods=["GET","POST"])
def login_page():
    session.clear()
    db.session.commit()
    session['user_id']=None
    session["email"]=None
    session["username"]=None
    session["on"]=1
    if request.method=="POST" or request.method=="GET":
        return render_template("login.html",option=1,invalid=0)

@app.route("/create_account/send_verification",methods=["GET","POST"])
def create_account():
    if request.method=="GET":
        return render_template("login.html",option=5, invalid=0)

@app.route("/create_account/verify_code", methods=["GET","POST"])
def verify_code():
    if request.method=="POST":
        session["email"]=request.form["email"]
        uf=userfunctions()
        a=uf.isalreadyuser(session['email'])
        if a[0]==1:
            uf.send_activation_verification(session["email"],a[1])
            session['gid']=a[1][1]
            return render_template("login.html",option=10,d=a[1])

        if uf.user_status(session["email"])==1:
            return render_template("login.html", option=8, key=1)
        else:
            uf.send_verification(session["email"])
            return render_template("login.html",option=6,inavlid=0)

@app.route("/activate_account/check_code", methods=["GET","POST"])
def activate_account_code():
    if request.method=="POST":
        passcode=request.form["verification_code"]
        uf=userfunctions()
        if uf.check_user(session["email"],passcode)==1:
            #continuing to creating account
            return render_template("login.html",option=11, mail=session["email"], invalid=0,gid=session['gid'] )
        else:
            #redirecting to enter verification code correctly
            return render_template("login.html",option=10, invalid=1,d=[session['email'],session['gid']])


@app.route("/create_account/check_code", methods=["GET","POST"])
def check_code():
    if request.method=="POST":
        passcode=request.form["verification_code"]
        uf=userfunctions()
        if uf.check_user(session["email"],passcode)==1:
            #continuing to creating account
            return render_template("login.html",option=7, mail=session["email"], invalid=0 )
        else:
            #redirecting to enter verification code correctly
            return render_template("login.html",option=6, invalid=1)

@app.route("/account_activated", methods=["GET","POST"])
def account_activated():
    #(username,name,dob,pp,p,cp,g)
    l=[request.form["name"],request.form["name"], request.form["dob"], request.files["profile_picture"].read(), request.form["password"], request.form["confirm_password"], request.form["flexRadioDefault"], session["gid"]]  
    uf=userfunctions()
    
    if l[4]==l[5]:
        uf.join_user(session["email"],l[0],l[1],l[2],l[4],l[3],l[6],l[7])
        return render_template("index_page.html",option=8)
    else:
        return render_template("index_page.html",option=7,invalid=1)
        

@app.route("/account_created", methods=["GET","POST"])
def account_created():
    #(username,name,dob,pp,p,cp,g)
    l=[request.form["name"],request.form["name"], request.form["dob"], request.files["profile_picture"].read(), request.form["password"], request.form["confirm_password"], request.form["flexRadioDefault"], request.form["gid"]]  
    uf=userfunctions()
    
    if l[4]==l[5]:
        uf.join_user(session["email"],l[0],l[1],l[2],l[4],l[3],l[6],l[7])
        return render_template("index_page.html",option=8)
    else:
        return render_template("index_page.html",option=7,invalid=1)
            
@app.route("/forgot_password",methods=["GET","POST"])
def forgot_password():
    if request.method=="GET":
        return render_template("login.html",option=2)

@app.route("/forgot_password/verify_code", methods=["GET","POST"])
def fp_send_verification():
    if request.method=="POST":
        mail=request.form["email"]
        session["email"]=mail
        uf=userfunctions()
        code=uf.forgot_send_verification(mail)
        if code==-1:
            return render_template("login.html",option=2,invalid=1)
        else:
            return render_template("login.html",option=3,invalid=0)
        

@app.route("/forgot_password/check_code", methods=["GET","POST"])
def fp_verify_code():
    if request.method=="POST":
        passcode=request.form["verification_code"]
        uf=userfunctions()
        if uf.check_user(session["email"],passcode)==1:
            #continue to resetting password
            return render_template("login.html",option=9, invalid=0)
            
        else:
            #verification code not matched 
            return render_template("login.html",option=3, inavlid=1)
            
@app.route("/forgot_password/check_password",methods=["GET","POST"])
def check_rp_password():
    if request.method=="POST":
        p=request.form["password"]
        cp=request.form["confirm_password"]
        if p==cp:
            uf=userfunctions()
            uf.fp_update_password(session["email"],p)
            session.clear()
            return render_template("login.html",option=4,invalid=0)
            #update password
        else:
            return render_template("login.html",option=9, invalid=1)



@app.route("/check", methods=["GET","POST"])
def check_login():
    print(request.method)
    if request.method=='POST':
        email=request.form["email"]
        password=request.form["password"]
        a=userfunctions().check_username(email)
        if a==-1:
            print("value of a",a)
            return render_template("login.html",option=1, invalid=1, nr=1)
        else:
            print("value of a",a)
            if a[1]==password:
                session["email"]=email
                if a[0]==None:
                    return render_template("login.html",option=7, key=1, data=a)
                else:
                    session["user_id"]=a[2]
                    session["username"]=a[0]
                    session['dpt_id']=a[5]
                    if a[6]==1:
                        session['superuser']=1
                    else:
                        session['superuser']=0
                    return redirect("/home")
            else:
                return render_template("login.html",option=1, invalid=1) 



@app.route("/account_modified", methods=["GET","POST"])
def account_modified():
    if session["on"]!=1:
        return redirect("/login")
    if request.method=="POST":
        email=session["email"]
        name=request.form["name"]
        dob=request.form["dob"]
        gender=request.form["flexRadioDefault"]
        pp=request.files["profile_picture"].read()
        session["user_id"]=userfunctions().modify_account(session["email"],name,dob,gender,pp)
        session["username"]=name
        session["on"]=1
        return redirect("/home")



@app.route("/logout", methods=["GET","POST"])
def logout():
    session.clear()
    return redirect("/login") 


@app.route("/home", methods=["GET","POST"])
def home():
    classfunctions().conflicts2()
    return render_template("home.html", option=1, un=session['username'],su=session['superuser'])



@app.route("/dashboard", methods=["GET","POST"])
def menu():
    #p=classfunctions().isconflict(2)
    return render_template("dashboard.html", un=session['username'], option=1,su=session['superuser'])


@app.route("/settings", methods=["GET","POST"])
def settings():
    return render_template("home.html",option=2, un=session['username'],su=session['superuser'])


@app.route("/update_account", methods=["GET","POST"])
def update_account():
    
    user_details=userfunctions().account_details(session["user_id"])
  
    return render_template("home.html",option=6,data=user_details,un=session['username'],su=session['superuser'])

@app.route("/update_account/update", methods=["GET","POST"])
def account_update():
    #print(request.form.keys)
        
    n=request.form['name']
    dob=request.form["dob"]
    m=request.form['m_number']
    g=int(request.form["flexRadioDefault"])
    pp=request.files["profile_picture"].read()
    pd=request.form['p_description']
    #r=request.form['role']
    r=''
    userfunctions().update_profile(session['email'],n,dob,g,pp,m,pd,r)
    
    session['username']=userfunctions().get_username(session['user_id'])

    return redirect("/account")


@app.route("/account", methods=["GET","POST"])
def account():
    #roomfunctions().add_dpts()
    #print(db.session.query(order.user_id).all())
    time_calc().add60('01:00')
    user_details=userfunctions().account_details(session["user_id"])
    ca=userfunctions().current_availability(int(session['user_id']))
    #print(ca)
    return render_template("home.html",option=8, data=user_details,  un=session['username'],ca=ca[0],userid=ca[1],su=session['superuser'])


@app.route("/dashboard/<int:id>",methods=["GET","POST"])
def department_dashboard(id):
    return render_template("dashboard.html", un=session['username'], option=0, sid=session['user_id'], did=int(id),su=session['superuser'])


@app.route("/my_dashboard",methods=["GET","POST"])
def my_dashboard():
    return render_template("dashboard.html", un=session['username'], option=0, sid=session['user_id'], did=session['dpt_id'],su=session['superuser'])



@app.route("/add_classroom",methods=["GET","POST"])
def add_a_class():
    f_ids=userfunctions().get_userid()
    rooms=roomfunctions().all_rooms()
    dpts=roomfunctions().all_dpts()
    acgs=groupsfunctions().all_cg_list(session['user_id'])
    return render_template("home.html",un=session['username'], option=7, acgs=acgs, rooms=rooms, fid=f_ids, dpt=dpts,su=session['superuser'])

@app.route("/add_classroom/add",methods=["GET","POST"])
def add_class():
    r=request.form['roomid']
    fid=request.form['fid']
    iid=request.form['iid']
    wd=request.form['wkd']
    et=request.form['e_time']
    st=request.form['s_time']
    temp=request.form['temporary']
    des=request.form['description']

    notify=request.form['notify']
    cgid=request.form['cgid']
    
    a=classfunctions().add_class(session['user_id'],r,fid,iid,wd,st,et,temp,des,0)

    classfunctions().notifybook(a[1],notify,cgid)

    return render_template("home.html", option=4, s=a[0], key=1,un=session['username'], sid=session['user_id'],su=session['superuser'])


@app.route("/dashboard/all_classrooms",methods=["GET","POST"])
def classrooms():
    a=classfunctions().all_classes()
    return render_template("dashboard.html",un=session['username'], data=a, option=2, sid=session['user_id'],su=session['superuser'])

@app.route("/dashboard/all_conflicts",methods=["GET","POST"])
def classconflicts():
    d=classfunctions().conflicts2()
    return render_template("dashboard.html",un=session['username'], d=d, option=5, sid=session['user_id'],su=session['superuser'])


@app.route("/dashboard/my_groups",methods=["GET","POST"])
def my_groups():
    d=groupsfunctions().all_groups(session['user_id'])
    return render_template("home.html",un=session['username'], data=d, option=13, sid=session['user_id'],su=session['superuser'])


@app.route("/dashboard/add_class_group",methods=["GET","POST"])
def add_class_group():
    return render_template("home.html",un=session['username'], option=5, sid=session['user_id'],su=session['superuser'])



@app.route("/dashboard/class_group_added",methods=["GET","POST"])
def class_group_added():
    cgn=request.form['cg_name']
    emi=request.form['emi']
    d=request.form['cgdescription']
    groupsfunctions().addgroup(cgn,session['user_id'],d,emi)
    return render_template("home.html",un=session['username'], option=3, sid=session['user_id'],det=cgn,cgadded=1,su=session['superuser'])


@app.route("/edit_class_group/<cgid>",methods=["GET","POST"])
def edit_class_group(cgid):
    data=groupsfunctions().get_cgdata(cgid)
    return render_template("home.html",un=session['username'], option=5,key=1, sid=session['user_id'],data=data,su=session['superuser'])




@app.route("/remove_class_group/<cgid>",methods=["GET","POST"])
def remove_class_group(cgid):
    data=groupsfunctions().remove_class_group(cgid)
    return redirect('/dashboard/my_groups')


@app.route("/dashboard/update_class_group/<cgid>",methods=["GET","POST"])
def edited_class_group(cgid):
    cgn=request.form['cg_name']
    emi=request.form['emi']
    d=request.form['cgdescription']
    groupsfunctions().update_classg(cgid,cgn,d,emi)
    return redirect('/view_class_group/'+cgid)


@app.route("/view_class_group/<cgid>",methods=["GET","POST"])
def view_class_group(cgid):
    d=groupsfunctions().get_all_cgdata(int(cgid))
    an=annfunctions().get_anndetails(int(cgid))
    return render_template("home.html",un=session['username'], option=14, sid=session['user_id'],data=d,an=an,su=session['superuser'])


@app.route("/dashboard/make_an_announcement/<cgid>",methods=["GET","POST"])
def make_an_announcement(cgid):
    d=groupsfunctions().get_cgdata(int(cgid))
    return render_template("home.html",un=session['username'], option=15, sid=session['user_id'],data=d,su=session['superuser'])

@app.route("/make_announcement/<cgid>",methods=["GET","POST"])
def make_announcement(cgid):
    new_msg=f'''
Dear students ,

{request.form['body']}

Thanks and Regards
{session['username']}
        '''
    annfunctions().add_announcement(request.form['subject'],cgid,new_msg)
    return render_template("home.html",un=session['username'], option=3, sid=session['user_id'],cgid=int(cgid),annsent=1,su=session['superuser'])



@app.route("/edit/<cid>",methods=["GET","POST"])
def edited_class(cid):
    f_ids=userfunctions().get_userid()
    rooms=roomfunctions().all_rooms()
    dpts=roomfunctions().all_dpts()
    d=classfunctions().details_for_edit(int(cid))
    return render_template("home.html",un=session['username'], option=10, cid=cid, rooms=rooms, fid=f_ids, dpt=dpts, d=d,su=session['superuser'])


@app.route("/edited/<cid>",methods=["GET","POST"])
def edit_a_class(cid):
    r=request.form['roomid']
    fid=request.form['fid']
    iid=request.form['iid']
    wd=request.form['wkd']
    et=request.form['e_time']
    st=request.form['s_time']
    temp=request.form['temporary']
    des=request.form['description']
    a=classfunctions().edit_class(cid,r,fid,iid,wd,et,st,temp,des)
    return redirect("/view_class/"+str(cid))

@app.route("/view_class/<cid>",methods=["GET","POST"])
def view_class(cid):
    k=classfunctions().isconflict(int(cid))
    #d=classfunctions().details_for_view(cid)
    print(k)
    if k[0]==1:
        e1=k[2]
        e2=k[3]
    else:
        b=[]
        e1=[]
        e2=[]
    return render_template("dashboard.html",un=session['username'],  option=4, sid=session['user_id'], data=k[1],key=k[0],e1=e1,e2=e2,su=session['superuser'])

@app.route("/dashboard/all_rooms",methods=["GET","POST"])
def all_rooms():
    k=classfunctions().availability_rooms()
    wday=time_calc().daycurr()[0]
    return render_template("dashboard.html",un=session['username'],  option=7, sid=session['user_id'], data=k, key=1,nkey=1,wday=wday,su=session['superuser'])

@app.route("/dashboard/search_all_rooms",methods=["GET","POST"])
def search_all_rooms():
    pattern=request.form['room_pattern']
    k=classfunctions().search_availability_rooms(pattern)
    wday=time_calc().daycurr()[0]
    return render_template("dashboard.html",un=session['username'],  option=7, sid=session['user_id'], data=k, key=1,pattern=pattern,wday=wday,su=session['superuser'])




@app.route("/dashboard/availability/search",methods=["GET","POST"])
def availability_search():
    #classfunctions().book_function_view(2)
    f_ids=userfunctions().get_userid()
    rooms=roomfunctions().all_rooms()
    dpts=roomfunctions().all_dpts()
    return render_template("dashboard.html",un=session['username'], data=[], option=8, rooms=rooms, fid=f_ids, dpt=dpts, sid=session['user_id'],su=session['superuser'])

@app.route("/dashboard/availability",methods=["GET","POST"])
def availability():
    
    st=request.form['s_time']
    et=request.form['e_time']
    wd=request.form['wkd']
    k=classfunctions().availability(wd,st,et)
    #print(k)
    return render_template("dashboard.html",un=session['username'],  option=7, sid=session['user_id'], wday=int(k[0]),stime=k[1],etime=k[2],data=k[3],su=session['superuser'])

@app.route("/dashboard/book/<rid>/<wdy>",methods=["GET","POST"])
def booking(rid,wdy):
    k=classfunctions().book_function_view(int(rid),int(wdy))
    f_ids=userfunctions().get_userid()
    rooms=roomfunctions().all_rooms()
    dpts=roomfunctions().all_dpts()
    acgs=groupsfunctions().all_cg_list(session['user_id'])
    return render_template("dashboard.html",un=session['username'], option=3, sid=session['user_id'],e1=k[0],e2=k[1],rid=rid,i=k[2][0],wkd=k[3], rooms=rooms, fid=f_ids, dpt=dpts,acgs=acgs,su=session['superuser'])

@app.route("/dashboard/book_class/<rid>/<wdy>",methods=["GET","POST"])
def book_class(rid,wdy):
    k=classfunctions().book_function_view(int(rid),int(wdy))
    r=int(rid)
    fid=request.form['fid']
    iid=request.form['iid']
    wd=int(wdy)
    et=request.form['e_time']
    st=request.form['s_time']
    temp=request.form['temporary']
    des=request.form['description']
    
    notify=request.form['notify']
    cgid=request.form['cgid']
    #print(notify,cgid)
    a=classfunctions().add_class(session['user_id'],r,fid,iid,wd,st,et,temp,des,1)
    
    classfunctions().notifybook(a,notify,cgid)
    return redirect("/view_class/"+str(a))



@app.route("/about",methods=["GET","POST"])
def about():
    #print(time_calc().pcn())
    #userfunctions().current_availability(1)
    #userfunctions().add_userids()
    #roomfunctions().insert_rooms()
    #classfunctions().enter_classes(session['user_id'])
    return render_template("home.html",un=session['username'], option=11, sid=session['user_id'],su=session['superuser'])


@app.route("/contact/", methods=["GET","POST"])
def contact():
    return render_template("home.html",option=9,msg=0,username=session["username"],un=session['username'],Name=session["username"],mail=session["email"],su=session['superuser'])

@app.route("/contact/send", methods=["GET","POST"])
def contact_send():
    emailTo().contactadmin(session["email"],session["username"],request.form["subject"],request.form["message"])
    return render_template("home.html", option=4, msg=1,k=1, key=1,un=session['username'], sid=session['user_id'],su=session['superuser'])



@app.route("/search_a_user", methods=["GET","POST"])
def search_a_user():
    pattern=request.form["pattern"]
    details=userfunctions().search_users(pattern,session["user_id"])
    return render_template("home.html", un=session["username"],option=12, d=details, key=1, f=1, pattern=pattern,su=session['superuser'])

@app.route("/user/<uid>", methods=["GET","POST"])
def users(uid):
    #print(session['user_id'],uid)
    if int(uid)==int(session["user_id"]):
        return redirect("/account")
    b=userfunctions().isuser_registered(int(uid))
    if b[0]:
            
        get_details=userfunctions().account_details(int(uid))
        #print(get_details,id)
        ca=userfunctions().current_availability(int(uid))
        return render_template("home.html",option=6,data=get_details,ca=ca[0],un=session['username'],key=1,userid=int(ca[1]),su=session['superuser'])
    else:
        return render_template("home.html",option=6,un=session['username'],notavail=1,det=b[1],su=session['superuser'])

@app.route("/user/gid/<gid>", methods=["GET","POST"])
def user_gid(gid):
    user_id=userfunctions().user_id_withgid(int(gid))
    return redirect('/user/'+str(user_id))
