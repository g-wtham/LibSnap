import cv2
from pyzbar.pyzbar import decode
import pyttsx3
import subprocess
import psycopg2 as postgres
from isbn_book_info import get_book_info
from email_alert import get_email
from email_alert import send_mail

def get_db_connection():
    return postgres.connect(
        database="libsnap", user="postgres", password="root", port=5432, host="localhost"
    )

def create_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql_query = '''
        CREATE TABLE IF NOT EXISTS scanned_records (
            id serial PRIMARY KEY,
            roll_number VARCHAR(30) NOT NULL,
            isbn_number VARCHAR(100),
            title VARCHAR(100),
            authors VARCHAR(300),
            pageCount INTEGER,
            categories VARCHAR(200),
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '15 days')
        );
        '''
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

create_table()

# Placeholder values (%s) instead of actual values in SQL query, which will be later passed as arguments in `cursor.execute`
def insert_data(qr_roll_no, isbn_number, title, authors, pageCount, categories):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql_query = '''
        INSERT INTO scanned_records (roll_number, isbn_number, title, authors, pageCount, categories) values (%s, %s, %s, %s, %s, %s); 
        '''
        cursor.execute(sql_query, (qr_roll_no, isbn_number, title, authors, pageCount, categories))
        conn.commit()
        conn.close()
        print(f"QR data '{qr_roll_no}' inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)


def scan_qr():
    engine = pyttsx3.init()
    cap = cv2.VideoCapture(1)
    
    '''
    Roll.no & isbn is set to None, so 1st scan we get 'roll_no'; 2nd scan we get 'isbn', until
    both data is got the data won't be inserted into the table.
    '''
    roll_no = None      
    isbn_number = None
    
    while True:
        ret, frame =  cap.read()
        if not ret:
            return
       
        barcodes = decode(frame)
       
        for barcode in barcodes:
            x1, y1, x2, y2 = barcode.rect
            # cv2.rectangle(frame, (x1, y1), (x1+x2, y1+y2), (255, 0, 0), 2)
            barcode_data = barcode.data.decode('utf-8')
            # cv2.putText(frame, barcode_data, (x1, y1-10), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)
            
            if roll_no is None:
                roll_no = barcode_data
                engine.say(f'Roll Number {barcode_data} is scanned.')
                engine.runAndWait()
                
            elif isbn_number is None:
                isbn_number = barcode_data
                engine.say(f'ISBN number is scanned.')
                engine.runAndWait()
                print("Roll. No: ", roll_no, "ISBN: ", isbn_number)
                
                # Importing and creating an instance of the function from `isbn_book_info.py``
                books_data = get_book_info(isbn_number)

                title = books_data['title']
                authors = books_data['authors']
                pageCount = books_data['pageCount']
                categories = books_data['categories']

                insert_data(roll_no, isbn_number, title, authors, pageCount, categories)
                print("Book information insertion successful!")
                
                result = None
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    email_query = '''SELECT email FROM new_users WHERE roll_number = %s LIMIT 1'''
                    cursor.execute(email_query, (roll_no, ))
                    result = cursor.fetchone()
                except Exception as e:
                    print("User does not exist! Sign UP")
                    print("\n", e)
                
                if result:  
                    due_date_query = '''SELECT due_date FROM scanned_records WHERE roll_number = %s LIMIT 1'''
                    cursor.execute(due_date_query, (roll_no, ))
                    result1 = cursor.fetchone()
                    db_due_date = result1[0]
                    send_mail(to_email=result[0], subject=f"Book Reminder for {roll_no}", text=f"You have borrowed the book '{title}' written by '{authors}'. \nYour book due date is on '{db_due_date}'.\n\nRegards,\nTeam LibSnap")
                    subprocess.run(['python', 'users.py'])
                else:
                    print("Email not found.")
                    engine.say("Email not found, please sign up with your email id to receive reminder.")
                    engine.runAndWait()
                    subprocess.run(['python', 'users.py'])
                    
                cursor.close()
                conn.close()
                # Reset variables for NEXT SCAN!
                roll_no = None
                isbn_number = None

        cv2.imshow("Barcode Scan - LibSnap", frame)
        # if barcodes:
        #     subprocess.run(['python', 'book_detect.py'])
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
           
scan_qr()