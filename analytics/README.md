# Analytics Module

## Overview

This module focuses on analyzing the Titanic dataset using Exploratory Data Analysis (EDA) and Machine Learning techniques. It includes data preprocessing, visualization, model training, performance evaluation, and model persistence.

## Dataset

- **Dataset:** Titanic
- **Rows:** 891
- **Columns:** 15

## Project Structure

```text
analytics/
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
├── best_pipeline.joblib
├── charts/
└── README.md
```

## Exploratory Data Analysis (EDA)

The EDA notebook includes:

- Dataset overview
- Missing value analysis
- Univariate analysis
- Bivariate analysis
- Multivariate analysis
- Correlation analysis
- Feature scaling

## Machine Learning Models

The following models were implemented and evaluated:

- Logistic Regression
- Decision Tree
- Random Forest
- Linear Regression

## Model Evaluation

The classification models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC Score

The regression model was evaluated using:

- MAE
- RMSE
- R² Score
- Adjusted R² Score

## Best Model

Logistic Regression achieved the best overall performance and was selected as the final model. The trained model was saved as **`best_pipeline.joblib`** for future use.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Joblib
- Imbalanced-learn