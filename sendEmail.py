import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pw import emailID, app_pw


def error_email_notify(log):
    msg = MIMEMultipart()
    msg.set_unixfrom('author')

    me = emailID
    you = 'minhhg16@gmail.com' 

    msg['From'] = me
    msg['To'] = you
    msg['Subject'] = '-----Auto Label Bot Error-----'

    message = log
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP_SSL('smtp.gmail.com')
    mailserver.ehlo()
    mailserver.login(emailID, app_pw)

    mailserver.sendmail(me,you,msg.as_string())
    mailserver.quit()
    print("done")