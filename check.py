import subprocess
import timeinterval
import cobra, cobra.io, cobra.test, csv,pandas,codecs, email, smtplib,sys
from email.mime.text import MIMEText
from cobra import Reaction, Metabolite, Model
pandas.options.display.max_rows = 100
from random import randint
import threading
import urllib.request,json
import urllib


def set_interval(func, sec):
    def func_wrapper():
        if func():
            set_interval(func, sec)
        else:
            return "it has been ended"
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def send_notification(message):
    values = {
        "content": message
    }

    headers = {
    'Content-Type': 'application/json',
    'X-Authorization': 'ML5U5PCQQ68A8ZHN52W4BHXKBWVNVF5TEYHYKLXLWJ5RQXDFWUEE7IJZ3HCPR1QC9G2H36YMY8XWE1973I7W55P9LHI2JX5L9N7C',
    'X-UserId': 'kovszasz'
    }
    request = urllib.request.Request('https://api.spontit.com/v3/push', data=json.dumps(values).encode('utf-8'), headers=headers)

    response_body = urllib.request.urlopen(request).read()
    print(response_body)
#    msg=MIMEText(message)
#    server = smtplib.SMTP('smtp.gmail.com', 587)
#    server.connect("smtp.gmail.com",587)
#    server.ehlo()
#    server.starttls()
#    server.ehlo()
#    server.login("kovszasz@gmail.com", "nederlandshaga")
#    text = msg.as_string()
#    server.sendmail("kovszasz@gmail.com", "kovszasz@gmail.com", text)
#    server.quit()

def checkScript():
    scriptName=sN
    # get running processes with the ps aux command
    res = subprocess.check_output(["ps","aux"], stderr=subprocess.STDOUT)
    ress=str(res)
    for line in ress.split("\n"):
        # if one of the lines lists our process
        if line.find("/usr/bin/python3 /usr/local/bin/ipython "+scriptName) ==-1:
            send_notification(message)
            return False
    return True
tint=sys.argv[1]
sN=sys.argv[2]
message = sys.argv[3]
set_interval(checkScript,3600*float(tint))
