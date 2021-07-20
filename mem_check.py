import subprocess
import timeinterval
import cobra, cobra.io, cobra.test, csv,pandas,codecs, email, smtplib,sys
from email.mime.text import MIMEText
from cobra import Reaction, Metabolite, Model
pandas.options.display.max_rows = 100
from random import randint
import threading,psutil,pickle
start_mem=psutil.virtual_memory().used
ended=False
global end_it
end_it=False
def saver(obj,name):
    f='/home/szabolcs/'
    outfile=open(f+name,'wb')
    pickle.dump(obj,outfile)
    outfile.close()

def loader(name):
    f='/home/szabolcs/'
    infile=open(f+name,'rb')
    return pickle.load(infile)

def set_interval(func, sec):
    def func_wrapper():
        if func():
            set_interval(func, sec)
        else:
            return "it has been ended"
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def send_mail(message):
    msg=MIMEText(message)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.connect("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("example@email.com", "password")
    text = msg.as_string()
    server.sendmail("example@email.com", "example@email.com", text)
    server.quit()

def checkScript():

    memory_usage.write(str(psutil.virtual_memory().used-start_mem)+'\n')
    memory_usage.flush()
    scriptName=sN
    # get running processes with the ps aux command
    res = subprocess.check_output(["ps","aux"], stderr=subprocess.STDOUT)
    ress=str(res)
    for line in ress.split("\n"):
        # if one of the lines lists our process
        if line.find(scriptName) ==-1:
           send_mail(scriptName+" has been finished")
           #saver(memory_usage,str(scriptName)+'_memory_profile')
           memory_usage.close()
           return False
    return True

tint=input('Check time interval:\t')
sN=input('Script Name:\t')
save=input('MEMfile:  ')
memory_usage=open(str(save)+'.txt','w')
set_interval(checkScript,3600*float(tint)) #the time_interval is in hours
