import psycopg2
import os
from flask import Flask, request
from dotenv import load_dotenv

# QUERIES
"""
  1. See book info
  2. Insert books
  3. Update books
  4. Add wishlist
  5. See wishlist
"""

# 1. Get only NECESSARY info of the books
GET_BOOK_INFO = '''
  SELECT
    B."Book_ID",
    B."Title",
    B."Edition",
    B."Synopsis",
    B."Publication_year",
    B."Pages",
    B."Rating",
    B."Stock",
    B."Price",
    P."Publisher_name",
    A."First_name" AS "Author_first_name",
    A."Last_name" AS "Author_last_name",
    L."Language_name" AS "Language_name",
    OL."Language_name" AS "Original_language_name",
    C."Category_name",
    BT."Type_name"
  FROM
    "Book" B
  JOIN
    "Publisher" P ON B."Publisher_code" = P."Publisher_code"
  JOIN
    "Author" A ON B."Author_ID" = A."Author_ID"
  JOIN
    "Language_Code" L ON B."Language_code" = L."Language_code"
  JOIN
    "Language_Code" OL ON B."Ori_language_code" = OL."Language_code"
  JOIN
    "Category" C ON B."Category_ID" = C."Category_ID"
  JOIN
    "Book_Type" BT ON B."Type_code" = BT."Type_code";
'''

# 2. Insert books
INSERT_INTO_BOOK = '''
  INSERT INTO "Book" (
    "Title",
    "Edition",
    "Synopsis",
    "Publisher_code",
    "Author_ID",
    "Publication_year",
    "Pages",
    "Rating",
    "Language_code",
    "Ori_language_code",
    "Stock",
    "Price",
    "Category_ID",
    "Type_code"
  )
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
'''

# 3. Update Book Info
UPDATE_BOOK_INFO_BY_ID = '''
  UPDATE "Book"
  SET
    "Edition" = %s,
    "Author_ID" = %s,
    "Publication_year" = %s,
    "Pages" = %s,
    "Stock" = %s,
    "Price" = %s,
    "Category_ID" = %s,
    "Title" = %s,
    "Rating" = %s,
    "Synopsis" = %s,
    "Publisher_code" = %s,
    "Language_code" = %s,
    "Ori_language_code" = %s,
    "Type_code" = %s
  WHERE "Book_ID" = %s;
'''

# 4. Add Into Wishlist
INSERT_INTO_WISHLIST = '''
  INSERT INTO "Wishlist" (
    "Customer_ID",
    "Book_ID"
  )
  VALUES (%s, %s);
'''

# 5. See Wishlist
GET_WISHLIST = '''
  SELECT W."Wishlist_ID", W."Customer_ID", C."First_name", C."Last_name", B."Title", B."Edition"
  FROM
    "Wishlist" W
  JOIN
    "Customer" C ON W."Customer_ID" = C."Customer_ID"
  JOIN
    "Book" B ON W."Book_ID" = B."Book_ID"
  ORDER BY "Customer_ID";
'''

app = Flask(__name__)

load_dotenv()
database = os.getenv("DATABASE_NAME")
host = os.getenv("HOST")
user = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
port = os.getenv("PORT")

connection = psycopg2.connect(database=database, host=host, user=user, password=password, port=port)

# 0. Home
@app.get('/')
def home():
  return 'Hello world!'

# 1. Get Book Information
@app.get('/api/book')
def get_books():
  try:
    with connection.cursor() as cursor:
      cursor.execute(GET_BOOK_INFO)
      books = cursor.fetchall()
    

    book_list= []
    for book in books:
      book_dict = {
        "Book_ID": book[0],
        "Title": book[1],
        "Edition": book[2],
        "Synopsis": book[3],
        "Publication_year": book[4],
        "Pages": book[5],
        "Rating": book[6],
        "Stock": book[7],
        "Price": book[8],
        "Publisher_name": book[9],
        "First_name": book[10],
        "Last_name": book[11],
        "Language_name": book[12],
        "Ori_language_name": book[13],
        "Category_name": book[14],
        "Type_name": book[15]
      }
      book_list.append(book_dict)
      
    return {"Books": book_list}, 200

  except Exception as e:
    return {"error": str(e)}, 500
  

# 2. Insert into Book table
@app.post('/api/book')
def insert_book():
  try:
    data = request.get_json()

    Edition = data['Edition']
    Author_ID = data['Author_ID']
    Publication_year = data['Publication_year']
    Pages = data['Pages']
    Stock = data['Stock']
    Price = data['Price']
    Category_ID = data['Category_ID']
    Title = data['Title']
    Rating = data['Rating']
    Synopsis = data['Synopsis']
    Publisher_code = data['Publisher_code']
    Language_code = data['Language_code']
    Ori_language_code = data['Ori_language_code']
    Type_code = data['Type_code']
    
    with connection:
      with connection.cursor() as cursor:
        cursor.execute("BEGIN;")
        cursor.execute(INSERT_INTO_BOOK, (
          Title,
          Edition,
          Synopsis,
          Publisher_code,
          Author_ID,
          Publication_year,
          Pages,
          Rating,
          Language_code,
          Ori_language_code,
          Stock,
          Price,
          Category_ID,
          Type_code
        ))

      connection.commit()
      return {"Message": "Operation executed successfully"}, 201
    
  except Exception as e:
    connection.rollback()
    return {"error": str(e)}, 400
  
# 3. Update Book Info
@app.put('/api/book/<int:book_id>')
def update_book(book_id):
  try:
    data = request.get_json()

    Edition = data['Edition']
    Author_ID = data['Author_ID']
    Publication_year = data['Publication_year']
    Pages = data['Pages']
    Stock = data['Stock']
    Price = data['Price']
    Category_ID = data['Category_ID']
    Title = data['Title']
    Rating = data['Rating']
    Synopsis = data['Synopsis']
    Publisher_code = data['Publisher_code']
    Language_code = data['Language_code']
    Ori_language_code = data['Ori_language_code']
    Type_code = data['Type_code']

    with connection.cursor() as cursor:
      cursor.execute("BEGIN;")
      cursor.execute(UPDATE_BOOK_INFO_BY_ID, (
        Edition,
        Author_ID,
        Publication_year,
        Pages,
        Stock,
        Price,
        Category_ID,
        Title,
        Rating,
        Synopsis,
        Publisher_code,
        Language_code,
        Ori_language_code,
        Type_code,
        book_id
      ))
    
    connection.commit()
    return {"message": f"Book with ID {book_id} updated succesfully"}, 200
    
  except Exception as e:
    connection.rollback()
    return {"error": str(e)}, 400
    
# 4. Add Into Wishlist
@app.post('/api/wishlist')
def insert_wishlist():
  try:
    data = request.get_json()

    Customer_ID = data['Customer_ID']
    Book_ID = data['Book_ID']

    with connection.cursor() as cursor:
      cursor.execute("BEGIN;")
      cursor.execute(INSERT_INTO_WISHLIST, (
        Customer_ID, Book_ID
      ))

    connection.commit()
    return {"message": f"Book with ID {Book_ID} added to wishlist for user {Customer_ID}"}, 201
  
  except Exception as e:
    connection.rollback()
    return {"error": str(e)}, 400
  
# 5. See wishlist of a customer
@app.get('/api/wishlist')
def get_customer_wishlist():
  try:
    with connection.cursor() as cursor:
      cursor.execute(GET_WISHLIST)
      wishlists = cursor.fetchall()

    wishlist_list = []

    for wishlist in wishlists:
      wishlist_dict = {
        "Wishlist_ID": wishlist[0],
        "Cust omer_ID": wishlist[1],
        "Name": {
          "First_name": wishlist[2],
          "Last_name": wishlist[3]
        },
        "Title": wishlist[4],
        "Edition": wishlist[5]
      }
      wishlist_list.append(wishlist_dict)

    return {"Wishlist": wishlist_list}, 200

  except Exception as e:
    return {"error": str(e)}, 500