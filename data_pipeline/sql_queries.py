from scraper import categories
import sqlite3
import pandas as pd

#connect to SQLite database
connection = sqlite3.connect("data_pipeline/database/books.db")
#create cursor
cursor = connection.cursor()

#Display all books with rating 5
query1 = """
SELECT title, rating
FROM books
WHERE rating = 5;
"""
print("\n======== QUERY 1 ========")
print(query1)
result = pd.read_sql(query1, connection)
print(result)

#Top 10 most expensive books
query2 = """
SELECT title, price_inr
From books
ORDER BY price_inr DESC
LIMIT 10;
"""
print("\n======== QUERY 2 ========")
print(query2)
result = pd.read_sql(query2, connection)
print(result)

#Display unique categories
query3 = """
SELECT DISTINCT category_name
FROM categories;
"""
print("\n======== QUERY 3 ========")
print(query3)
result = pd.read_sql(query3, connection)
print(result)

#Books with rating between 3 and 5
query4 = """
SELECT title, rating
FROM books
WHERE rating BETWEEN 3 AND 5;
"""
print("\n======== QUERY 4 ========")
print(query4)
result = pd.read_sql(query4, connection)
print(result)

#Join books and categpries tables
query5 = """
SELECT b.title, c.category_name,
    b.rating, b.price_inr
FROM books b
JOIN categories c
ON b.category_id = c.category_id
ORDER BY b.rating DESC
LIMIT 10;
"""
print("\n======== QUERY 5 ========")
print(query5)
result = pd.read_sql(query5, connection)
print(result)


#Read complete tables into pandas Dataframes
books_df = pd.read_sql("SELECT * FROM books;", connection)
categories_df = pd.read_sql("SELECT * FROM categories;", connection)

print("\n========== BOOKS DATAFRAME ==========")
print(books_df.head())
print("\n========== CATEGORIES DATAFRAME ==========")
print(categories_df.head())

#Reproduce the SQL JOIN using pandas merge
merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)

#select only the required columns
merged_df = merged_df[
    ["title", "category_name", "rating", "price_inr"]
]

#sort to match SQL query output
merged_df = merged_df.sort_values(
    by="rating",
    ascending=False
)

print("\n======== PANDAS MERGE RESULT ========")
print(merged_df.head(10))

connection.close()