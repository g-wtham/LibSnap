from ultralytics import YOLO
import cv2
from google import genai
from google.genai import types
import PIL.Image
import numpy as np 
import os
from dotenv import load_dotenv

load_dotenv()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

model = YOLO("./models/best.pt")

classNames = ["book"]

book_detected = False 

while True and not book_detected:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame")
        break
        
    results = model(img)
    
    cv2.imshow("Book Detection", img)

    for r in results:
        boxes = r.boxes

        for box in boxes:
            confidence = box.conf[0].item()
            if confidence >= 0.78:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.imshow("Book Detection", img)  
                cv2.waitKey(1)  

                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                image = PIL.Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=['''Analyze the image and determine if it contains a PUBLISHED BOOK cover. 
                                A published book is a commercially produced book with an ISBN or similar identifier, 
                                not a handwritten notebook or journal

                                OUTPUT REQUIREMENTS:
                                1. If a clear book cover is visible, return a JSON object with these fields:
                                - title: The complete title of the book
                                - author: The author name(s) if visible
                                - valid: true
                                
                                2. If no book cover is visible or the image is unclear, return:
                                {"valid": false, "message": "No valid book detected in image"}''', image])

                print(response.text)
                book_detected = True  
                break  # Exit the inner loop
        
        if book_detected:
            break  # Exit the outer results loop

    if cv2.waitKey(1) == ord('q'):
        break
    import time
    time.sleep(0.2)

cap.release()
cv2.destroyAllWindows()