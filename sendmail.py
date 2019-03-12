# build the mail
from email.mime.text import MIMEText
from email.header import Header
import smtplib

def SendEmail(to_addr, From="", To="", Subject="", Message="Hello!"):
    msg = MIMEText(Message, 'plain', 'utf-8')
    msg['From'] = Header(From, 'utf-8')
    msg['To'] = Header(To, 'utf-8')
    msg['Subject'] = Header(Subject, 'utf-8')
    from_addr = 'your mail'
    password = 'your pass word'
    server = 'smtp.qq.com'


    server = smtplib.SMTP(server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

if __name__ == "__main__":
    SendEmail('from mail')
