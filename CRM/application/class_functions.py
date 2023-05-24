from .database import db
from .local_time import *
from .models import classes
from .announcement_functions import *

class classfunctions:


    def lapping(self,l,p,t,i):
        if p>=1:
            if l[p][0]<l[p-1][1]:

                o=[l[p][0],l[p][1],l[p-1][0],l[p-1][1]]
                t+=[o]
                ##print(o,t)
                temp=[min(o),max(o),l[p][2]+l[p-1][2]]
                l=l[:p-1]+[temp]+l[p+1:]
                #print("yes")
                return classfunctions().lapping(l,p-1,t,i-1)
            else:
                return t,l,i
        else:
            return t,l,i

    def overlap(self,a):
        k=[]
        for i in range(len(a)):
            
            k+=[[a[i][1],a[i][2],a[i][0]]]
        k.sort()
        #print(len(k))
        #print(k)
        #p={}
        c=0
        i=1
        while i<len(k):
            #print(i,k)
            if k[i][0]<k[i-1][1]:
                t,k,i=classfunctions().lapping(k,i,[],i)
            else:
                c+=1
                #p[c]=[k[i]]
            i+=1
        return k

    def process(self,a):
        return int(a[:2]+a[3:])

    def reprocess(self,a,b):
        return str(a)[:2]+':'+str(a)[2:],str(b)[:2]+':'+str(b)[2:]

    def conflicts(self):
        rooms=db.session.execute('select room_id from rooms')
        rooms=rooms.fetchall()
        c={}
        k={}
        #print(rooms)
        for i in rooms:
            t=db.session.execute("select r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id and c.room_id=:rid",{"rid":i[0]})
            t=t.fetchall()
            c[i[0]]=t
            temp=[]
            for j in t:
                temp+=[[[j[13]],classfunctions().process(j[6]),classfunctions().process(j[7])]]
            k[i[0]]=temp
        p={}
        c=1
        for i in k:
            q=classfunctions().overlap(k[i])
            for j in q:
                if len(j[2])>1:
                    p[c]=[i,j[2]]
                    c+=1
            #print("function",classfunctions().list_of_conflicts(q))
            #print("q",q)
            #print("p",p)
        rc=[] 
        for i in p:
            g=[]
            for j in p[i][1]:
                u=db.session.execute("select r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id and c.room_id=:rid and c.class_id=:cid",{"rid":p[i][0],"cid":j})
                g+=[u.fetchall()]
            rc+=[g]
        #print(rc)
        return rc

    def list_of_conflicts(self,a):
        p=[]
        w=[]
        for i in a:
            if len(i[2])>1:
                p+=[i[2]]
                w+=i[2]
        return p,w

    def add_class(self,uid,r,fid,iid,wd,st,et,temp,des,key):
        nst,net=classfunctions().nstnet(st,et)
        before_e=db.session.execute("select count(conflicted) from classes where conflicted=1 group by conflicted")
        before_e=before_e.fetchall()
        if len(before_e)==0:
            before_e=0
        else:
            before_e=before_e[0][0]

        t=time_calc().time()
        du=time_calc().duration(st,et)
        db.session.execute("insert into classes(room_id,created_by,faculty_id,incharge_id,session_time,weekday,start_time,end_time,temporary,remarks,created_time,last_update,st,et) values(:rid,:uid,:fid,:iid,:du,:w,:st,:et,:temp,:r,:ti,:ti,:nst,:net)",{"rid":r,"uid":uid,"fid":fid,"iid":iid,"w":wd,"st":st,"et":et,"du":du,"temp":temp,"r":des,"ti":t,"nst":nst,"net":net})
        db.session.commit()
        classfunctions().conflicts2()
        after_e=db.session.execute("select count(conflicted) from classes where conflicted=1 group by conflicted")
        after_e=after_e.fetchall()
        if len(after_e)==0:
            after_e=0
        else:
            after_e=after_e[0][0]

        if key==0:
            a=db.session.execute("select class_id from classes where room_id=:rid and created_by=:uid and faculty_id=:fid and incharge_id=:iid and session_time=:du and weekday=:w and start_time=:st and end_time=:et and temporary=:temp and remarks=:r and created_time=:ti and last_update=:ti",{"rid":r,"uid":uid,"fid":fid,"iid":iid,"w":wd,"st":st,"et":et,"du":du,"temp":temp,"r":des,"ti":t,"nst":nst,"net":net})
            a=a.fetchall()
          
            if after_e>before_e:
                return 1,a[0][0]
            elif after_e<before_e:
                return -1,a[0][0]
            else:
                return 0,a[0][0]
        else:
            a=db.session.execute("select class_id from classes where room_id=:rid and created_by=:uid and faculty_id=:fid and incharge_id=:iid and session_time=:du and weekday=:w and start_time=:st and end_time=:et and temporary=:temp and remarks=:r and created_time=:ti and last_update=:ti",{"rid":r,"uid":uid,"fid":fid,"iid":iid,"w":wd,"st":st,"et":et,"du":du,"temp":temp,"r":des,"ti":t,"nst":nst,"net":net})
            a=a.fetchall()
            return a[0][0]

    def notifybook(self,cid,n,cg):
        if cg!='':
            print('class id',cid,n)
            db.session.execute("update classes set cg_id=:cgid where class_id=:cid",{"cgid":int(cg),"cid":cid})
            db.session.commit()
            if int(n)==1:
                a=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                b=[ 'It is a Permanent Class','It is a Temporary Class']
                details=db.session.execute("select r.room_no,c.created_by,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,u.name from classes c, user u, rooms r where r.room_id=c.room_id and u.user_id=c.created_by and c.class_id=:cid",{"cid":cid})
                details=details.fetchall()[0]
                print(details)
                sub='Regarding session creation by '+str(details[11])
                msg=f'''
Dear all,

Session created by {details[11]} on {details[10]}.

Room Number : {details[0]}
Created by : {details[11]} {details[2]}
Faculty ID : {details[2]}
Incharge ID : {details[3]}
Weekday : {a[int(details[5])]}
Start Time : {details[6]}
End Time : {details[7]}
Session Duration : {details[4]}

{b[int(details[8])]}

{details[9]}

Thanks and Regards
Manikanta Sandeep
Team Project CRMS.
        '''
                print(sub,msg)
                return annfunctions().add_announcement(sub,int(cg),msg)
                
        return


    def nstnet(self,s,e):
        nst,net=(str(s),str(e))
        nst,net=(int(nst[:2]+nst[3:]),int(net[:2]+net[3:]))
        return nst,net

    def manipulate_all(self):
        a=db.session.execute("select class_id from classes")
        a=a.fetchall()
        #print(a)
        for i in a:
            p=db.session.execute("select start_time,end_time from classes where class_id=:i",{"i":i[0]})
            p=p.fetchall()[0]
            #print(p)
            nst,net=classfunctions().nstnet(p[0],p[1])
            db.session.execute("update classes set st=:nst, et=:net where class_id=:i",{"nst":nst,"net":net,"i":i[0]})
            db.session.commit()
        return

    def all_classes(self):
        a=db.session.execute("select r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.conflicted,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id")
        a=a.fetchall()
        return a

    def conflicts2(self):
        rooms=db.session.execute('select room_id from rooms')
        rooms=rooms.fetchall()
        
        c={}
        for m in [0,1,2,3,4,5,6]:
            k={}
            for i in rooms:
                
                t=db.session.execute("select start_time,end_time,class_id,room_id from classes where room_id=:rid and weekday=:m",{"rid":i[0],"m":m})
                t=t.fetchall()
                #print("room id: ",i[0],"Weekday: ",m,"t: ",t)
                
                temp=[]
                for j in t:
                    temp+=[[[j[2]],classfunctions().process(j[0]),classfunctions().process(j[1])]]
                if len(temp)!=0:
                    k[i[0]]=temp
            if len(k.keys())!=0:
                c[m]=k
        #print(c)
        week_room=c.copy()
        new_wr=week_room.copy()
        conf=[]
        conflict_id=[]
        #print("Week Room",week_room)
        for k in week_room:
            for i in week_room[k]:
                q=classfunctions().overlap(week_room[k][i])
                x,ids=classfunctions().list_of_conflicts(q)
                if len(x)!=0:
                    #print(x)
                    conf+=x
                    conflict_id+=ids

        conf.sort()
        conflict_id.sort()
        db.session.execute("update classes set conflicted=0")
        db.session.commit()
        a=classes.query.filter(classes.class_id.in_(conflict_id)).update({'conflicted':1})
        
        db.session.commit()
        conf2=conf.copy()
        #for i in conf:
        #print(conf)
        for i in range(len(conf)):
            for j in range(len(conf[i])):
                u=db.session.execute("select r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id and c.class_id=:cid",{"cid":conf[i][j]})
                conf2[i][j]=u.fetchall()[0]
        #print(conf2)
        return conf2

    def clean_dic(self,d):
        p={}
        for i in d.keys():
            if len(d[i].keys())==0:
                continue
            else:
                temp={}
                for j in d[i].keys():
                    if len(d[i][j])==0:
                        continue
                    else:
                        temp[j]=d[i][j]
                if len(temp.keys())==0:
                    continue
                p[i]=temp
            
        return p

            
    def edit_class(self,cid,r,fid,iid,wd,et,st,temp,des):
        before_e=db.session.execute("select count(conflicted) from classes where conflicted=1 group by conflicted")
        before_e=before_e.fetchall()
        if len(before_e)==0:
            before_e=0
        else:
            before_e=before_e[0][0]
        od=db.session.execute("select room_id,created_by,faculty_id,incharge_id,session_time,weekday,start_time,end_time,temporary,remarks,created_time,last_update from classes where class_id=:cid",{"cid":cid})
        od=od.fetchall()[0]
        t=time_calc().time()
        if r!='':
            r1=r
        else:
            r1=od[0]
        if fid!='':
            fid1=fid
        else:
            fid1=od[2]
        if iid!='':
            iid1=iid
        else:
            iid1=od[3]
        if wd!='':
            wd1=wd
        else:
            wd1=od[3]
        if st!='':
            st1=st
        else:
            st1=od[6]
        if et!='':
            et1=et
        else:
            et1=od[7]
        if temp!='':
            temp1=temp
        else:
            temp1=od[8]
        if des!='':
            des1=des
        else:
            des1=od[9]
        du=time_calc().duration(st1,et1)
        db.session.execute("update classes set room_id=:r1,faculty_id=:fid1,incharge_id=:iid1,session_time=:du,weekday=:wd1,start_time=:st1,end_time=:et1,temporary=:temp1,remarks=:des1,last_update=:t where class_id=:cid",{"cid":cid,"r1":r1,"fid1":fid1,"iid1":iid1,"du":du,"wd1":wd1,"st1":st1,"et1":et1,"temp1":temp1,"des1":des1,"t":t})
        db.session.commit()
        classfunctions().conflicts2()
        after_e=db.session.execute("select count(conflicted) from classes where conflicted=1 group by conflicted")
        after_e=after_e.fetchall()
        if len(after_e)==0:
            after_e=0
        else:
            after_e=after_e[0][0]
        if after_e>before_e:
            return 1
        elif after_e<before_e:
            return -1
        else:
            return 0
        

    def details_for_edit(self,cid):
        a=db.session.execute("select c.room_id,r.room_no, c.faculty_id,c.incharge_id, c.weekday, c.start_time, c.end_time, c.temporary, c.remarks from classes c, rooms r where r.room_id=c.room_id and c.class_id=:cid",{"cid":cid})
        a=a.fetchall()[0]
        return a

    def details_for_view(self,cid):
        a=db.session.execute("select r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.conflicted,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id and c.class_id=:cid",{"cid":cid})
        a=a.fetchall()
        return a

    def return_interval(self,l,cid):
        #print("Test here",l)
        for i in l:
            if (cid in i[2]) and len(i[2])>1:
                return i
        return -1

    def return_interval2(self,l):
        for i in l:
            print(i)
            if len(i[2])>1:
                return i
        return -1

    def enter_classes(self,uid):
        l=[['08:00', '09:00', 0, 'CSD V LAB', 600541, 20], ['08:00', '09:00', 1, 'WAD', 120016, 10], ['08:00', '09:00', 2, 'EEM', 10021, 10], ['08:00', '09:00', 3, 'BOM', 600577, 23], ['08:00', '09:00', 4, 'BOM', 600577, 23], ['09:00', '10:00', 0, 'CSD V LAB', 600541, 20], ['09:00', '10:00', 1, 'BOM', 600577, 23], ['09:00', '10:00', 3, 'WAD', 120016, 10], ['10:00', '11:00', 0, 'AI', 600566, 10], ['10:00', '11:00', 1, 'EEM', 10021, 10], ['10:00', '11:00', 2, 'WAD LAB', 120016, 18], ['10:00', '11:00', 3, 'CC LAB', 600395, 9], ['10:00', '11:00', 4, 'CD', 600344, 14], ['11:00', '12:00', 0, 'CD', 600344, 14], ['11:00', '12:00', 2, 'WAD LAB', 120016, 18], ['11:00', '12:00', 3, 'CC LAB', 600395, 9], ['11:00', '12:00', 4, 'AI', 600566, 10], ['12:00', '13:00', 4, 'ML', 600629, 14], ['13:00', '14:00', 0, 'CC', 600395, 10], ['13:00', '14:00', 1, 'ML', 600629, 14], ['13:00', '14:00', 2, 'CC', 600395, 10], ['14:00', '15:00', 0, 'CSD V VA', 600425, 14], ['14:00', '15:00', 1, 'CD', 600344, 14], ['14:00', '15:00', 2, 'ML LAB', 600629, 11], ['14:00', '15:00', 3, 'CD LAB', 600344, 6], ['15:00', '16:00', 0, 'CSD V QA', 600405, 14], ['15:00', '16:00', 1, 'AI', 600566, 10], ['15:00', '16:00', 2, 'ML LAB', 600629, 11], ['15:00', '16:00', 3, 'CD LAB', 600344, 6], ['15:00', '16:00', 4, 'EEM', 10021, 10]]

        for i in l:
            t=time_calc().time()
            nst,net=classfunctions().nstnet(i[0],i[1])
            duration=time_calc().duration(i[0],i[1])
            db.session.execute("insert into classes(start_time,end_time,weekday,remarks,faculty_id,incharge_id,room_id,created_by,session_time,temporary,created_time,last_update,st,et) values(:st,:et,:w,:r,:fid,:iid,:rid,:cby,:sst,:t,:ct,:lu,:nst,:net)",{'st':i[0],'et':i[1],'w':i[2],'r':i[3],'fid':i[4],'iid':i[4],'rid':i[5],'cby':uid,'sst':duration,'t':0,'ct':t,'lu':t,'nst':nst,'net':net})
            db.session.commit()
        classfunctions().conflicts2()
        return

    def percentage_p(self,l):
        p=time_calc().act_time2(l[0][0],l[0][1])
        q=[[l[0],'']]
        diff=(p[1]-p[0])/8
        nl=[p[0]-diff,p[1]+diff]
        adiff=(p[1]-p[0])
        for i in range(1,len(l)):
            t=time_calc().act_time2(l[i][0],l[i][1])
            #print("t",t)
            a=((t[0]-nl[0])/adiff)*100
            b=((t[1]-t[0])/adiff)*100
            c=((nl[1]-t[1])/adiff)*100
            #print(a,b,c)
            q+=[[[a,b,c],l[i]]]
        #print(q)
        return q

    def isconflict(self,cid):
        u=db.session.execute("select weekday,room_id from classes where class_id=:cid",{"cid":cid})
        u=u.fetchall()[0]
        wday=u[0]
        rid=u[1]
        #print(u,wday,rid)
        allrw=db.session.execute("select class_id, start_time, end_time from classes where weekday=:w and room_id=:rid",{"w":wday,"rid":rid})
        allrw=allrw.fetchall()
        #print(allrw)
        temp=[]
        for i in allrw:
            temp+=[[[i[0]],classfunctions().process(i[1]),classfunctions().process(i[2])]]
        a=classfunctions().overlap(temp)
        #print(a)
        b=classfunctions().return_interval(a,cid)
        if b==-1:
            a=classfunctions().details_for_view(cid)
            return -1,a
        else:
            out=classes.query.filter(classes.class_id.in_(b[2]))
            out2=db.session.execute("select  r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.conflicted,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id and c.class_id in "+str(tuple(b[2])))
            out2=out2.fetchall()
            #print("b[0],b[1]",b[0],b[1])
            qo=time_calc().act_time(b[0],b[1])
            b[0],b[1]=qo[0][0],qo[0][1]
            te=[list(qo[1])+['']]
            
            for i in out2:
                te+=[[i[6],i[7],i[14]]]
            e=classfunctions().percentage_p(te)
            return 1,out2,e[0],e[1:]

    def search_class(self,wd,st,et,ast,aet):
        t=time_calc().daycurr()
        if st!='':
            st1=classfunctions().process(st)
        else:
            st1=t[1]
        if et!='':
            et1=classfunctions().process(et)
        else:
            et1=st1
        d=db.session.execute("select r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.conflicted,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id and c.weekday=:wkd and c.st<=:st and c.et>=:et",{"wkd":t[0],"st":int(st1),"et":int(et1)})
        d=d.fetchall()
        wday=t[0]
        #print(u,wday,rid)
        allrw=db.session.execute("select class_id, start_time, end_time from classes where weekday=:w ",{"w":wday})
        allrw=allrw.fetchall()
        #print('allrw',st1,et1)
        rst1,ret1=classfunctions().reprocess(st1,et1)
        temp=[[[''],int(st1),int(et1)]]
        for i in allrw:
            temp+=[[[i[0]],classfunctions().process(i[1]),classfunctions().process(i[2])]]
        #print(temp)
        a=classfunctions().overlap(temp)
        print(a)
        b=classfunctions().return_interval2(a)
        #print("new",b[0],b[1])
        '''if b==-1:
            a=classfunctions().details_for_view(cid)
            return -1,a
        else:
            out=classes.query.filter(classes.class_id.in_(b[2]))
            out2=db.session.execute("select  r.room_no,u.name,c.faculty_id,c.incharge_id,c.session_time,c.weekday,c.start_time,c.end_time,c.temporary,c.remarks,c.created_time,c.last_update,c.created_by,c.conflicted,c.class_id from classes c, rooms r, user u where u.user_id=c.created_by and c.room_id=r.room_id and c.class_id in "+str(tuple(b[2])))
            out2=out2.fetchall()
            #print("b[0],b[1]",b[0],b[1])
            qo=time_calc().act_time(b[0],b[1])
            #print("qo",qo)
            b[0],b[1]=qo[0][0],qo[0][1]
            te=[list(qo[1])+['']]
            
            for i in out2:
                te+=[[i[6],i[7],i[14]]]
            ##print("b",b)
            e=classfunctions().percentage_p(te)
            return 1,out2,e[0],e[1:]
'''
    def availability(self,wd,st,et):
        t=time_calc().daycurr()
        if st!='':
            st2=st
            st1=classfunctions().process(st)
        else:
            st2=t[2]
            st1=t[1]
        if et!='':
            et1=classfunctions().process(et)
            etime=et
        else:
            et2=time_calc().add60(st2)
            et1=et2[1]
            etime=et2[0]
        if int(wd)==-1:
            wd=int(t[0])
        d=db.session.execute("select room_id from rooms")
        d=d.fetchall()
        print("Day",wd)
        t=[]
        print("time",st1,et1)
        for i in d:
            td=db.session.execute("select room_id from classes where ((st<=:st1 and et>=:et1) or (st<=:st1 and et>=:st1) or (st<=:et1 and et>=:et1)) and room_id=:rid and weekday=:wid",{"rid":i[0],"st1":st1,"et1":et1,"wid":wd})
            td=td.fetchall()
            print("td",td,"i[0]",i[0])
            for i in td:
                t+=[i[0]]
            p=set(t)
            p=list(p)
        print("what is p",p)
        if len(p)==1:
            p='('+str(p[0])+')'
        elif len(p)==0:
            p='('+str(-1)+')'
        else:
            p=tuple(p)
        print(p)
        #avi=[]
        for i in p:
            avi=db.session.execute("select r.room_id,r.room_no, r.dpt_id, d.dpt_name, d.description,r.description,r.date_joined from rooms r, department d where d.dpt_id=r.dpt_id and r.room_id not in "+str(p))
            avi=avi.fetchall()
        return [wd,st2,etime,avi]
        
    def book_function_view(self,rid,wdy):
        a=db.session.execute('select class_id, start_time,end_time from classes where room_id=:rid and weekday=:wkd',{"wkd":wdy,"rid":rid})
        a=a.fetchall()
        te=[['00:00','23:59','']]
        for i in a:
            te+=[[i[1],i[2],i[0]]]
        print("b",te)
        e=classfunctions().percentage_p(te)
        #print(e)
        avi=db.session.execute("select r.room_id,r.room_no, r.dpt_id, d.dpt_name, d.description,r.description,r.date_joined from rooms r, department d where d.dpt_id=r.dpt_id and r.room_id=:rid ",{"rid":rid})
        avi=avi.fetchall()
        return e[0],e[1:],avi,wdy
        
    def availability_rooms(self):
        avi=db.session.execute("select r.room_id,r.room_no, r.dpt_id, d.dpt_name, d.description,r.description,r.date_joined from rooms r, department d where d.dpt_id=r.dpt_id")
        avi=avi.fetchall()
        return avi

    def search_availability_rooms(self,pattern):
        query="select r.room_id,r.room_no, r.dpt_id, d.dpt_name, d.description,r.description,r.date_joined from rooms r, department d where d.dpt_id=r.dpt_id and r.room_no like "+"'%"+pattern+"%'"
        avi=db.session.execute(query)
        avi=avi.fetchall()
        return avi