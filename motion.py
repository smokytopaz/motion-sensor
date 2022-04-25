import sys
import RPi.GPIO as GPIO
import datetime as dt
from datetime import datetime, timedelta
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Set up RPi - Check appropriate pins are used
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#For PIR Sensor
GPIO.setup(11, GPIO.IN)
#For LED
GPIO.setup(3, GPIO.OUT)

alertEmail = []

#Creates an initial start time for the compareTime function
start_time = datetime.today()
alertEmail.insert(0,start_time)
print(alertEmail[0])

def timestamp():
    stamp = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    return stamp

def compareTime():
    #Timeout value in minutes
    n = 10
    #Current time plus the timeout value
    next_alert = alertEmail[0] + timedelta(minutes = n)

    #Compares the last alert time with the current time
    compTime = next_alert >= datetime.now()

    if (compTime == False):
#        print("Send Email")
        alertEmail.insert(0,datetime.today())
        return(False)

def alertTimez():
    #Set time 24hr
    start = dt.time(20,0,0)
    #Set time 24hr
    end = dt.time(6,30,0)
    now = datetime.now().time()
    #Use when times go overnight
    return now >= start or now <= end
    #Use for same day
    #return start <= now <= end

#Consider putting this in a log file        
def logz():
    if compareTime() == False:
        print(timestamp(),"- Motion Detected [Location]")
        if (alertTimez() == True):
            alertz()
        #Use for DEBUG
        else:
            print("Outside of alertTimez")

def alertz():
    mail_from = 'example@example.com'
    mail_to = 'example@example.com'
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = mail_to
    msg['Subject'] = 'Motion Detected [Location]'
    mail_body = 'Movement has been detected [Specific Location Detail]'
    msg.attach(MIMEText(mail_body))

    try:
        server = smtplib.SMTP_SSL('smtp.sendgrid.net', 465)
        server.ehlo()
        server.login('login', 'password')
        server.sendmail(mail_from, mail_to, msg.as_string())
        server.close()
        #Use for DEBUG
        print('mail sent')
    except Exception as e:
        print(e)

def dummyLight(motion):
    motion = i
    if i == 0:
        #use print for DEBUG
        #print(timestamp(),"- No Motion Detected"),i
        GPIO.output(3,0)
        time.sleep(0.1)
    elif i == 1:
        #use print for DEBUG
        #print(timestamp(),"- Motion Detected"),i
        GPIO.output(3,1)
        time.sleep(0.1)

while True:
    i = GPIO.input(11)
    dummyLight(i)
    if i == 1:
        logz()
