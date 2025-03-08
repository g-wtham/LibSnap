Forgot the due date for books you took from the library? LibSnap remembers so you don't end up paying fines!

The main purpose of LibSnap is to solve the common problem of students forgetting to return books on time and incurring late fees.

It creates a digital record of borrowed books and proactively reminds students when books need to be returned, helping both students save money and libraries maintain their collections.

Cherry on the top, this entire setup works without using any PAID tools.. 

![image](https://github.com/user-attachments/assets/c92278ca-332b-4c15-968f-e4f2f208512e)

### Video Demo :

https://github.com/user-attachments/assets/35d5c234-4618-453b-a24f-b0bfefa2dfb5

### Here's what it does:

1. The system first scans barcode in <br>
    i. Student IDs <br>
   ii. ISBN barcode in the borrowed book

In each step, a sound alert is given to signal the user that correct data has been captured.

Fetches book details from Google Books/Open Library API using the ISBN number present in ISBN barcode, which lies at bottom-corner in the backcover of every published book! Thus associating the borrowed book’s title & author with the user's roll number.

2. In cases where book ISBN barcodes are damaged (or) back covers are damaged, hold the book cover in front of the camera, the custom trained YOLOv11n model [(on books covers)](https://colab.research.google.com/drive/11phX3oV7EO5itm9awyoucHTpt3-groo8) detects the book, gets the image, then LibSnap uses Gemini API to recognize book covers and extract title and author information, to associate with the user.

![LibSnap - Book OCR](https://github.com/user-attachments/assets/02ded859-0c8c-404e-9a2d-69f3779be9b7)

4. All borrowing records are stored in a PostgreSQL database, automatically setting due dates 15 days from checkout and tracking all lending activity, and sends timely reminders to the registered email ID.

5. Students can access a web portal to view all their borrowed books and due dates in one place. If it's a new user, he/she has to sign up first! And it's a one time process, as successive borrowed books get associated in that account.

### Data Flow :

ISBN barcode → Query Google Books/Open Library API → Get book metadata <br>
Cover image → YOLO model book detection → Gemini API → Extract title/author

![image](https://github.com/user-attachments/assets/c1c18432-9b83-4e5c-8dde-e8b9d8677b30)

## Automatic Email Reminders :
![{8B587C2A-2D7C-4537-A4D7-2E73D5B248E5}](https://github.com/user-attachments/assets/85a31541-7512-4607-bf7f-d9a124a638c6)

### Real-World Usage :

➡️ Scenario: New Student Registration

1. New student visits the library, takes the book and during his exit
2. A QR code is placed near this setup, which contains a link to our web portal to register.
3. Students provide roll number, email, password.
4. Account is created for future book checkouts
5. Scans the book, student ID and rest of the workflow is discussed above..

### Setup Requirements :

1.  Hardware: 
   - Computer with webcam
   - Barcode/QR code scanner (optional, can use webcam)

2.  Software Dependencies: 
   - PostgreSQL database
   - Python libraries: OpenCV, pyzbar, pyttsx3, psycopg2, Flask, YOLO v11 Nano
   - Google Gemini API (for OCR)
   - Gmail account credentials (for sending emails)


### Initial Stage :

https://github.com/user-attachments/assets/42552fc7-5a3d-4d9c-b123-2dfd57e323bf



ID & Book Detection - Uncut Version : 

https://github.com/user-attachments/assets/5030b85e-59fa-46b3-86b0-e6885e3a7108
