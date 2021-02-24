import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time

EMAIL = os.getenv("EMAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def current_milli_time():
    return round(time.time() * 1000)

def send_mail(from_email, receiver, subject, message):

    me = EMAIL
    my_password = EMAIL_PASSWORD
    you = receiver

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = you

    html = message
    part2 = MIMEText(html, 'html')

    msg.attach(part2)

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('mail.privateemail.com')
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already
    s.login(me, my_password)

    s.sendmail(me, you, msg.as_string())
    s.quit()

# send_mail("devwithme@devwithme.xyz", "Not Important Update", "<h1>Hope this still get inserted to the database though!</h1>")

