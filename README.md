# Zepto Data & AI Platform

An end-to-end AI/ML platform built as a capstone project for the Zepto analytics guild.

The project contains three connected modules:

1. Data Pipeline
2. Analytics & Machine Learning
3. GenAI Support Assistant

---

## Project Structure


zepto-data-ai-platform/
│
├── data_pipeline/
│   ├── data/
│   ├── database/
│   ├── scraper.py
│   ├── sql_queries.py
│   └── README.md
│
├── analytics/
│   ├── charts/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── best_pipeline.joblib
│   ├── titanic.csv
│   └── README.md
│
├── support_assistant/
│   ├── app/
│   ├── docs/
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md

---

## Module 1 — Data Pipeline

The data pipeline collects book data from an online source, cleans and transforms the data, and stores the data in a relational SQLite database.

### Features
* Web scraping using Python
* Data cleaning and transformation
* Price conversion to INR
* CSV data storage
* SQLite database
* Relational tables for books and categories
* SQL queries and Pandas analysis

### Run
```bash
cd data_pipeline
python scraper.py
python sql_queries.py
```

---

## Module 2 — Analytics & Machine Learning

This module performs exploratory data analysis and machine learning using the Titanic dataset.

### Features
* Data loading and validation
* Missing-value analysis
* Outlier analysis
* Univariate analysis
* Multivariate analysis
* Correlation analysis
* Feature preprocessing
* Classification models
* Model evaluation
* Confusion matrices
* ROC curves
* Residual analysis
* Saved machine-learning pipeline

### Main Files
* [01_eda.ipynb]-Exploratory Data Analysis
* [02_modeling.ipynb] — Machine Learning
* [best_pipeline.joblib] — Saved trained pipeline
* [titanic.csv] — Offline dataset
* [charts/] — Generated visualizations

---

## Module 3 — GenAI Support Assistant

The Support Assistant is a policy-grounded question-answering API for Zepto.

It retrieves relevant information from Zepto policy documents and generates an answer with source documents and confidence information.

### Features
* FastAPI REST API
* LangGraph workflow
* ChromaDB vector retrieval
* Sentence-transformer embeddings
* Policy document ingestion
* Intent classification
* Source-aware answers
* Offline mock LLM mode
* Docker containerization

### Run Locally
```bash
cd support_assistant

python -m venv .venv
```
Activate the virtual environment and install dependencies:
```bash
# On Windows
.venv\Scripts\activate
# On Unix/macOS
source .venv/bin/activate

pip install -r requirements.txt
```
Run the API:
``` bash
uvicorn main:app --reload --port 8000
```
Open the API documentation:
* http://localhost:8000/docs

### Docker
Build the Docker image:
```bash
cd support_assistant
docker build -t zepto-support-assistant .
```
Run the container:
```bash
docker run -d -p 8000:8000 --name zepto-support zepto-support-assistant
```
Open the API documentation:
* http://localhost:8000/docs

---

## Design Decisions

### Data Pipeline
The pipeline separates scraping, transformation, and database operations. SQLite is used as a lightweight relational database suitable for local development and analysis.

### Analytics
The analytics workflow separates exploratory data analysis from model development. Data preprocessing and model development are organized to support reusable and reliable machine-learning workflows.

### Support Assistant
The support assistant uses retrieval-based responses so that answers are grounded in the provided Zepto policy documents. LangGraph manages the workflow between intent classification, document retrieval, and response generation.

---

## Technologies
* Python
* Pandas
* NumPy
* SQLite
* SQL
* Scikit-learn
* Matplotlib
* Seaborn
* LangGraph
* ChromaDB
* Sentence Transformers
* FastAPI
* Docker

## Project Status

| Module             | Status       |
|--------------------|--------------|
| Data Pipeline      | Completed    |
| Analytics & ML     | Completed    |
| Support Assistant  | Completed    |
| Docker Deployment  | Completed    |

## Author

**Vishnuvardhan Gali**  
B.Tech — CSE (Data Science)  
TKR College of Engineering and Technology