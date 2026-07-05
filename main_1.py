import smtplib
from email.message import EmailMessage
import RPi.GPIO as GPIO
import time

emailhost = 'your.emailserver.com'
username = 'name@domain.com'
password = 'mypassword'

def sendEmail(subject, body, to):    
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['from'] = username
    msg['to'] = to
    s = smtplib.SMTP_SSL(emailhost)
    s.login(username, password)
    s.send_message(msg)
    s.quit()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Reed Switch on pin 18
GPIO.setup(21, GPIO.OUT) #Buzzer on pin 21
p = GPIO.PWM(21, 200)
p.ChangeFrequency(80)

prevState = False #default to on
try:
    while True:
        input_state = GPIO.input(18)
        if input_state == True:
            print('Reed switch off')
            if input_state != prevState:
                print("email alert, door open")              
                sendEmail("Door open alert","Your door was opened.","2155551212@vtext.com") #Subject, Body, Recipient
                p.start(1) # start the buzzer
                for i in range(800,1800,100): #a buzz runs from low to high
                    p.ChangeFrequency(i)
                    time.sleep(0.05)
                p.ChangeFrequency(80) #buzz hums low while door is open
        else:
            print("Reed switch closed; door is closed")
            if input_state != prevState:
                print("Stop buzzing.")
                p.stop() #no more buzz
        time.sleep(0.2) #polling interval / wait period
        prevState = input_state
except KeyboardInterrupt:
    print("kill program")
    GPIO.cleanup()


