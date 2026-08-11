# 📚 Data Pipeline Module

## Zepto Data & AI Platform – Capstone Project

### Overview

The Data Pipeline module is responsible for collecting, cleaning, transforming, and storing product data in a structured relational database.

For this capstone, the public **Books to Scrape** website is used as the data source to simulate a real-world product catalog pipeline. The extracted data is cleaned, enriched with currency conversion, stored in a normalized SQLite database, and queried using SQL and Pandas.

---

# Objectives

- Scrape product data from multiple categories
- Handle multi-page pagination
- Clean and transform raw data
- Convert GBP prices into INR
- Store data in a normalized relational database
- Execute SQL queries
- Perform SQL and Pandas-based data analysis

---

# Data Source

**Website**

https://books.toscrape.com/

This website is publicly available for web scraping practice and does not require authentication or an API.

---

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Requests | Download HTML pages |
| BeautifulSoup | HTML Parsing |
| Pandas | Data Cleaning & Analysis |
| SQLite3 | Relational Database |

---

# Folder Structure

```text
data_pipeline/
│
├── data/
│   └── books.csv
│
├── database/
│   └── books.db
│
├── scraper.py
├── sql_queries.py
└── README.md
```

---

# Features Implemented

### Web Scraping

- Extracted books from **4 categories**
- Implemented automatic pagination
- Scraped **144 books**

### Data Cleaning

Performed the following transformations:

- Removed currency symbol (£)
- Converted price into float (`price_gbp`)
- Converted text ratings into integers (1–5)
- Converted availability into boolean values
- Converted GBP to INR

### Error Handling

Invalid numeric parsing is handled using `try-except`.

If any row cannot be parsed correctly, it is skipped to ensure that the pipeline continues executing without interruption.

---

# Currency Conversion

A fixed project-defined conversion rate was used.

```text
1 GBP = 105.50 INR
```

No external API was used.

---

# Database Design

The database follows a normalized schema consisting of two related tables.

## Categories Table

| Column | Type |
|---------|------|
| category_id | INTEGER PRIMARY KEY |
| category_name | TEXT UNIQUE |

---

## Books Table

| Column | Type |
|---------|------|
| book_id | INTEGER PRIMARY KEY |
| title | TEXT |
| price_gbp | REAL |
| price_inr | REAL |
| rating | INTEGER |
| in_stock | INTEGER |
| category_id | INTEGER (Foreign Key) |

---

# SQL Operations

The following SQL concepts have been implemented.

- SELECT
- WHERE
- ORDER BY
- LIMIT
- DISTINCT
- BETWEEN
- INNER JOIN

---

# Executed SQL Queries & Outputs

The following SQL queries are implemented and executed using SQLite and Pandas.

### Query 1 — Books with Rating 5

```sql
SELECT title, rating
FROM books
WHERE rating = 5;
```

Output: Displays all books with a rating of 5.

### Query 2 — Top 10 Most Expensive Books

```sql
SELECT title, price_inr
FROM books
ORDER BY price_inr DESC
LIMIT 10;
```

Output: Displays the 10 most expensive books based on INR price.

### Query 3 — Unique Categories

```sql
SELECT DISTINCT category_name
FROM categories;
```

Output: Displays all unique book categories.

### Query 4 — Books with Rating Between 3 and 5

```sql
SELECT title, rating
FROM books
WHERE rating BETWEEN 3 AND 5;
```

Output: Displays books having ratings from 3 to 5.

### Query 5 — Books with Categories

```sql
SELECT b.title, c.category_name,
       b.rating, b.price_inr
FROM books b
JOIN categories c
ON b.category_id = c.category_id
ORDER BY b.rating DESC
LIMIT 10;
```

Output: Displays the top 10 books by rating along with their category and INR price.

---

# Pandas Operations

The following Pandas operations were implemented.

- `pd.read_sql()`
- `pd.merge()`

The SQL JOIN result was successfully reproduced using Pandas Merge.

---

# Generated Files

Running the project automatically generates:

```text
data/books.csv
database/books.db
```

---

# Installation

Clone the repository.

```bash
git clone <repository-url>
```

Move into the project folder.

```bash
cd zepto-data-ai-platform
```

Install dependencies.

```bash
pip install requests beautifulsoup4 pandas
```

---

# Execution

Run the scraper.

```bash
python data_pipeline/scraper.py
```

Run SQL queries.

```bash
python data_pipeline/sql_queries.py
```

---

# Expected Output

After successful execution:

- 144+ books are scraped
- CSV dataset is generated
- SQLite database is created
- SQL queries execute successfully
- Pandas reproduces the SQL JOIN result

---

# Learning Outcomes

This module demonstrates:

- Web Scraping
- Data Cleaning
- Feature Engineering
- Relational Database Design
- SQL Querying
- Pandas Data Analysis
- End-to-End Data Pipeline Development

---

# Author

**Vishnuvardhan Gali**

Certificate Program in Artificial Intelligence & Machine Learning
