import requests

def get_book_info(isbn_number):
    google_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_number}"
    google_response = requests.get(google_url)
    google_data = google_response.json()

    if "items" in google_data and google_data["items"]:
        google_book = google_data["items"][0]["volumeInfo"]
        return {
            'title': google_book.get("title", "Unknown Book"),
            'authors': google_book.get("authors", ["Unknown Author"]),
            'pageCount': google_book.get("pageCount", "Unknown Pages"),
            'categories': google_book.get("categories", ["Unknown Category"]),
            'publish_date': google_book.get("publishedDate", "Unknown Date"),
            'publisher': google_book.get("publisher", "Unknown Publisher")
        }

    openlibrary_url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn_number}&format=json&jscmd=data"
    openlibrary_response = requests.get(openlibrary_url)
    openlibrary_data = openlibrary_response.json()

    key = f"ISBN:{isbn_number}"
    if key in openlibrary_data:
        openlibrary_book = openlibrary_data[key]
        return {
            'title': openlibrary_book.get("title", "Unknown Book") + 
                     (": " + openlibrary_book.get("subtitle", "Unknown Subtitle")),
            'authors': openlibrary_book.get("authors", ["Unknown Author"]),
            'pageCount': openlibrary_book.get("pageCount", "Unknown Pages"),
            'categories': openlibrary_book.get("categories", ["Unknown Category"]),
            'publish_date': openlibrary_book.get("publishedDate", "Unknown Date"),
            'publisher': openlibrary_book.get("publisher", "Unknown Publisher")
        }

    return {"error": "Book not found in both Google Books and Open Library"}