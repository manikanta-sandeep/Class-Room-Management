import smtplib
import time
import email
import random

from .userfunctions import *

class emailTo:
    def generate_password(self):
        l1=[]
        for i in range(10):
            l1+=[str(i)]
        password=""
        for i in range(8):
            password+=random.choice(l1)
        return password

    def contactadmin(self,mail,name,subject,msg):
        message=f'''
Hi Admin,

There is a query from {name}
    Name    : {name}
    Email   : {mail}

Message:

{msg}

Thanks and Regards,
Team Project SRP.
        '''
        emailTo().send_email(subject,"projectsrp.manikanta@gmail.com",message)
        return

    def send_email(self,subject,reciever,msg):
        start = time.time()
        
        try:
            smtp_ssl = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        except Exception as e:
            smtp_ssl = None
        
        r_code, r = smtp_ssl.login(user="projectsrp.manikanta@gmail.com", password="camqcojiyaxiisbn")
        r_code, r = smtp_ssl.verify(reciever)
        #print(r_code,r)
        message = email.message.EmailMessage()
        message.set_default_type("text/plain")

        frm = "Project SRP"
        to_list = reciever
        message["From"] = frm
        message["To"] = to_list
        message["Subject"] = subject

        message.set_content(msg)

        r = smtp_ssl.sendmail(from_addr=frm,
                                    to_addrs=to_list,
                                    msg=message.as_string())

        