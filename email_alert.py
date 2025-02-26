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
