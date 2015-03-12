import imaplib
import smtplib
import email
from HTMLParser import HTMLParser
from email.parser import HeaderParser
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys 

def get_first_text_block(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()

def read(username,password):
	#Connect to Gmail Server
	try:
		mailserver = imaplib.IMAP4_SSL('imap.gmail.com', 993)
	except:
		print("[-] Failed to connect to mailserver")
		sys.exit(0)

	#Login with the given username and password
	try:
		mailserver.login(username,password)
	except:
		print("[-] Failed to login with given credentials")
		sys.exit(0)

	status, count = mailserver.select("Inbox")
	status, data = mailserver.fetch(count[0],'(RFC822)')
	raw_email = data[0][1]
	email_message = (email.message_from_string(raw_email))
	mailserver.close()
	return get_first_text_block(email_message)

def send(username,password,toaddr,message):
	msg = MIMEMultipart()
	msg["From"] = username
	msg["To"] = toaddr
	msg["Subject"] = "Stock selling"
	text = message
	msg.attach(MIMEText(text))
	server = smtplib.SMTP("smtp.gmail.com",25)
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(username, toaddr, msg.as_string())
	server.quit()