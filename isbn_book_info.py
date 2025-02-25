import requests

def get_book_info(isbn_number):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_number}")
    data = response.json()
    
    # if `items` KEY (not an value - key::value pair) not found, then google books doesn't have the data of this book
    if "items" not in data:
        print("Book not found.")
        return
            
    # Selects the `items` dictionary from the `data` json object..       
    books_json = data["items"][0]["volumeInfo"]
    
    return {
        'title' : books_json.get("title", "unknown_book"),
        'authors' : books_json.get("authors", ["unknown_author"]),
        'pageCount' : books_json.get("pageCount", "unknown_pages"),
        'categories' : books_json.get("categories", "unknown_category"),
    }