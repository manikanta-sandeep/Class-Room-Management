from datetime import datetime,timedelta
import pytz



class time_calc:
    def time(self):
        UTC = pytz.utc
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        return datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z')
    def time_with(self,start,end):
        start_time=datetime.strptime(start, '%Y:%m:%d %H:%M:%S %Z')
        end_time=datetime.strptime(end, '%Y:%m:%d %H:%M:%S %Z')
        difference=end_time-start_time 
        minutes=(difference.seconds)//60
        hours=(difference.seconds)//3600
        days=difference.days
        weeks=days//7
        months=days//30
        years=months//12
        seconds=difference.seconds
        return minutes,hours,days,weeks,months,years,seconds

    def duration(self,s,e):
        start_time=datetime.strptime(s, '%H:%M')
        end_time=datetime.strptime(e, '%H:%M')
        difference=end_time-start_time
        difference=end_time-start_time 
        #print('Time see',difference.seconds,(difference.seconds)%60,(difference.seconds)//3600)
        if difference.seconds>=3600:
            minutes=(difference.seconds)%60
            hours=(difference.seconds)//3600
        else:
            minutes=(difference.seconds)//60
            hours=(difference.seconds)//3600
        return str(hours)+"hrs :"+str(minutes)+"mins"

    def act_time(self,s,e):
        s,e=str(s),str(e)
        ##print("s, e",s[:2],s[2:],e[:2],e[2:])
        if len(s)==3:
            s='0'+s
        if len(e)==3:
            e='0'+e
        s1=s[:2]+":"+s[2:]
        e1=e[:2]+":"+e[2:]
        
        print('s1,e1',s1,e1)
        stime=datetime.strptime('00:00', '%H:%M')
        start_time=datetime.strptime(s1, '%H:%M')
        end_time=datetime.strptime(e1, '%H:%M')
        d1=start_time-stime
        d2=end_time-stime
        return [[d1.seconds/60,d2.seconds/60],[s1,e1]]
        
    def daycurr(self):
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        ct=datetime_ist.strftime('%H%M')
        act=datetime_ist.strftime('%H:%M')
        #print(ct)
        a=datetime_ist.weekday()
        return [a,ct,act]

    def act_time2(self,s,e):
        s,e=str(s),str(e)
        stime=datetime.strptime('00:00', '%H:%M')
        start_time=datetime.strptime(s, '%H:%M')
        end_time=datetime.strptime(e, '%H:%M')
        d1=start_time-stime
        d2=end_time-stime
        return [d1.seconds/60,d2.seconds/60]

    def add60(self,s):
        s=str(s)
        #print("S",s)
        start_time=datetime.strptime(s, '%H:%M')
        #print(start_time)
        e=start_time+ timedelta(hours=1)
        e=e.strftime('%H:%M'),int(e.strftime('%H%M'))
        #print(e)
        return e

    def sub60(self,s):
        s=str(s)
        #print("S",s)
        start_time=datetime.strptime(s, '%H:%M')
        #print(start_time)
        e=start_time- timedelta(hours=1)
        e=e.strftime('%H:%M'),int(e.strftime('%H%M'))
        #print(e)
        return e

    def pcn(self):
        IST = pytz.timezone('Asia/Kolkata')
        t = datetime.now(IST)
        wday=t.weekday()
        t=t.strftime('%H:%M')
        pre=time_calc().sub60(t)
        nex=time_calc().add60(t)
        e=datetime.strptime(t, '%H:%M')
        e=e.strftime('%H:%M'),int(e.strftime('%H%M'))
        return pre,e,nex,wday


    def convert(self,s):
        #print(time_calc().time())
        e=time_calc().time()
        (a,b,c,d,f,g,h)=time_calc().time_with(s,e)
        #print("seconds",h,"minutes",a,"hours",b,"days",c,"weeks",d,"months",f,"years",g)
        if g>=1:
            temp=str(g)
            if g==1:
                temp=temp+" year"
            else:
                temp=temp+" years"
        elif f>=1:
            temp=str(f)
            if f==1:
                temp=temp+" month"
            else:
                temp=temp+" months"
        elif d>=1:
            temp=str(d)
            if d==1:
                temp=temp+" week"
            else:
                temp=temp+" weeks"
        elif c>=1:
            temp=str(c)
            if c==1:
                temp=temp+" day"
            else:
                temp=temp+" days"
        elif b>=1:
            temp=str(b)
            if b==1:
                temp=temp+" hour"
            else:
                temp=temp+" hours"
        elif a>=1:
            temp=str(a)
            if a==1:
                temp=temp+" minute"
            else:
                temp=temp+" minutes"
        else:
            temp=str(h)
            if h==1:
                temp=temp+" second"
            else:
                temp=temp+" seconds"
        return temp+" ago"


    