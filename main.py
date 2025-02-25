import cv2
from pyzbar.pyzbar import decode
import pyttsx3
import subprocess

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
            engine.say(barcode_data)
            engine.runAndWait()


        cv2.imshow("barcode", frame)
        if barcodes:
            subprocess.run(['python', 'book_detect.py'])
       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()
           
scan_qr()