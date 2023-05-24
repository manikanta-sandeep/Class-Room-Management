from .database import db 
from .local_time import *
from .analysis import *
from .models import order, inventory, item, user

start="2023:01:26 00:00:00 IST"
class graphs:
    def draw_graphs_of(self,uid):
        inv_l=db.session.execute("select inventory_id from inventory where user_id=:uid",{"uid":uid})
        e=inv_l.fetchall()
        p=[]
        if len(e)!=0:
            for i in e:
                p+=[i[0]]
        a=order.query.filter(order.inventory_id.in_(p)).all()
        c=[]
        x=[]
        y=[]
        for i in a:
            x+=[i.quantity_required]
            y+=[time_calc().time_with(start,i.ordered_time)]
        
        
        time_units = ["minutes", "hours", "days", "weeks", "months", "years", "seconds"]
        for i in range(len(time_units)):
            temp=[]
            for j in y:
                temp+=[j[i]]
           
            analyze().plot_an(temp,x,time_units[i])
        return
