import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

# Fixed project-defined GBP to INR conversion rate
GBP_TO_INR = 105.50

# Map website rating words to integer values from 1 to 5
RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
} 

# Send a GET request to the Books to Scrape website
response = requests.get(BASE_URL, timeout=30)

# Check whether the website request was successful
print("Status Code:", response.status_code)

# Parse the HTML content received from the website
soup = BeautifulSoup(response.text, "html.parser")

# Find all book category links from the sidebar
category_links = soup.select(".side_categories ul li ul li a")

# Print the total number of categories found
print("Total Categories Found:", len(category_links))

# Display the first few category names
for category in category_links[:5]:
    print(category.text.strip())

# Create an empty list to store category names and URLs
categories = []

# Extract the name and URL of every available category
for category in category_links:
    category_name = category.text.strip()
    category_url = BASE_URL + category["href"]

    categories.append({
        "category": category_name,
        "url": category_url
    })

# Display the first three categories to verify the extracted data
print("\nFirst 3 Categories:")
for category in categories[:4]:
    print(category)

#scrape the first three categories
selected_categories = categories[:4]
all_books = []

for category in selected_categories:
    print(f"\nScraping Category: {category['category']}")
    #start scraping from the first page of the seleted category
    current_page = category["url"]
    #continue scraping untill there are no more pages
    while current_page:

    # Send a request to the selected current page
        category_response = requests.get(current_page, timeout=30)
        category_response.raise_for_status()

        category_soup = BeautifulSoup(category_response.text, "html.parser")

        # extract all the book cards from the current page
        book_cards = category_soup.select("article.product_pod")

        print(f"Category: {category['category']}")
        print(f"Current Page URL: {current_page}")
        print(f"Books in this page: {len(book_cards)}")

   
    #Extract data frome every book on the current page
        for book in book_cards:
            #Extract the book title
            title=book.h3.a["title"]
            #Extract and clean the price
            price_text = book.select_one(".price_color").text.strip()
            price_gbp = float(price_text.replace("£", "").replace("Â", ""))

            #Convert rating into an integer
            rating_text = book.select_one(".star-rating")["class"][1]
            rating=RATING_MAP[rating_text]

            #convert stock status into boolean
            availability_text = book.select_one(".availability").text.strip()
            in_stock = "In stock" in availability_text

            #convert GBP to INR
            price_inr = round(price_gbp * GBP_TO_INR,2)

            #store the cleaned book information in a dictionary
            book_data={
                "title": title,
                "category": category["category"],
                "price_gbp": price_gbp,
                "rating" : rating,
                "in_stock": in_stock,
                "price_inr": price_inr
                }

            #Add the dictionary to the list
            all_books.append(book_data)

        #verify the stored data
        print(f"Total books collected so far: {len(all_books)}")

        #check wether the current category has a next page
        next_button = category_soup.select_one("li.next a")

        if next_button :
            #Build the absolute URL of the next page
            current_page = urljoin(current_page,next_button["href"])
            
        else:
            #Stop pagination when no next page exists
            current_page=None


# Convert the scraped data into a pandas DataFrame
books_df = pd.DataFrame(all_books)

# Save the cleaned dataset as a CSV file
books_df.to_csv(
    "data_pipeline/data/books.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nData successfully saved to data_pipeline/data/books.csv")
print(f"Total Books Scraped: {len(books_df)}")
print(books_df.head())


#connect to the SQLite database 
connection = sqlite3.connect("data_pipeline/database/books.db")

#create a cursor to execute SQL queries
cursor = connection.cursor()

#creaye the categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
     category_id INTEGER PRIMARY KEY AUTOINCREMENT,
     category_name TEXT UNIQUE NOT NULL
     )
""")
# Create the books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL NOT NULL,
    price_inr REAL NOT NULL,
    rating INTEGER NOT NULL,
    in_stock INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id)
    REFERENCES categories(category_id)
)
""")

# Clear existing data before inserting fresh records
cursor.execute("DELETE FROM books")
cursor.execute("DELETE FROM categories")
connection.commit()

#Insert unique categories into the categories table
for category in books_df["category"].unique():
    cursor.execute("""
    INSERT OR  IGNORE INTO categories (category_name)
    VALUES (?)
    """,(category,))

#save inserted category 
connection.commit()

#create a mapping betwwen category name and category
cursor.execute("""
SELECT category_id, category_name
FROM categories
""")

category_map = {
    category_name: category_id
    for category_id, category_name in cursor.fetchall()
}
print(category_map)

#Insert every book into the books table
for _, row in books_df.iterrows():

    cursor.execute("""
    INSERT INTO books (
        title,
        price_gbp,
        price_inr,
        rating,
        in_stock,
        category_id
    )
    VALUES(?,?,?,?,?,?)
    """,
    (
        row["title"],
        row["price_gbp"],
        row["price_inr"],
        row["rating"],
        int(row["in_stock"]),
        category_map[row["category"]]
            
    ))


#save all database changes
connection.commit()
#close the database connection
connection.close()

print("\nData inserted successfully into SQLite database.")
