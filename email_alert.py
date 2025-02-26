from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os 

load_dotenv()

username = os.getenv("GMAIL_ID")
password = os.getenv("GMAIL_PASS")

def get_email(conn, roll_no):
    cursor = conn.cursor()
    email_query = '''SELECT email FROM students_details WHERE roll_number = %s'''
    cursor.execute(email_query, (roll_no, ))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]

def send_mail(to_email, subject, text):
    if to_email is None:
        return

    msg = MIMEText(text, 'plain')
    msg["From"] = username
    msg['To'] = to_email
    msg["Subject"] = subject    

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(from_addr=username, to_addrs=to_email, msg=msg.as_string())
        print(f"Email sent successfully to {to_email}")
