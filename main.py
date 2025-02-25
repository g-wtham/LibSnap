import cv2
from pyzbar.pyzbar import decode
import pyttsx3
import subprocess
import psycopg2 as postgres

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
            roll_no VARCHAR(30) NOT NULL,
            scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

create_table()

def insert_data(qr_roll_no):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql_query = '''
        INSERT INTO scanned_records (roll_no) values (%s);
        '''
        cursor.execute(sql_query, (qr_roll_no, ))
        conn.commit()
        conn.close()
        print(f"QR data '{qr_roll_no}' inserted successfully!")
    except Exception as e:
        print("Error inserting data:", e)


def scan_qr():
    engine = pyttsx3.init()
    cap = cv2.VideoCapture(0)
    
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
            print(barcode_data)
            insert_data(barcode_data)
            engine.say(barcode_data)
            engine.runAndWait()


        cv2.imshow("barcode", frame)
        # if barcodes:
        #     subprocess.run(['python', 'book_detect.py'])
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
           
scan_qr()