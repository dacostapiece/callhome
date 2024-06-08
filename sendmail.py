import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import mailserver, mailusername, mailpassword, source_mailaddress, dest_mailaddress, mailsubject_success, smtpport, mailsubject_failed, smtpport

def send_mail_my_ip_is(currentIpAddress):
  
    subject = mailsubject_success + currentIpAddress
    body = "This is an automated email.\n\nMy current IP address is: " + currentIpAddress

    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = mailsubject_success + currentIpAddress

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(mailserver, smtpport)
        server.starttls()
        server.login(mailusername, mailpassword)
        text = msg.as_string()
        server.sendmail(source_mailaddress, dest_mailaddress, text)

        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

def send_mail_vpn_failed():
    body = "This is an automated email.\n\nThe VPN connection has failed."

    msg = MIMEMultipart()
    msg['From'] = source_mailaddress
    msg['To'] = dest_mailaddress
    msg['Subject'] = mailsubject_failed

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(mailserver, smtpport)
        server.starttls()
        server.login(mailusername, mailpassword)
        text = msg.as_string()
        server.sendmail(source_mailaddress, dest_mailaddress, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

# Example usage:
# send_mail_my_ip_is("192.168.1.10")
# send_mail_vpn_failed()
