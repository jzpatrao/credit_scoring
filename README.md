# credit_classification
<<<<<<< HEAD
This is a FastApi api for a classification model. 

The API utilizes a logistic regression model with specific parameters and follows a preprocessing pipeline to classify loan applications. The purpose of this API is to facilitate the accurate and efficient classification of loan applications based on various features. The evaluation metrics employed include the AUC score and a custom-made error_cost_score that addresses the financial impact of false negatives and false positives.

## Feature Selection:
The SelectKBest algorithm is used to select the most relevant features for the classification task, based on their statistical significance.

## Model Details
The classification model used in the API is a logistic regression model. The model is trained with the following parameters:
- Penalty: L2
- Class Weight: Auto
- C: 10
- Solver: lbfgs

## Preprocessing Steps
The loan application data undergoes several preprocessing steps before being fed into the model. These steps are encapsulated within a pipeline and include the following operations:

1. One Hot Encoder
2. Imputation  (median strategy)
3. SMOTE (Synthetic Minority Over-sampling Technique)
4. Standard Scaler


## Evaluation Metrics
The Loan Application Classification API employs two evaluation metrics to assess the performance of the model:

1. AUC Score: The Area Under the Receiver Operating Characteristic (ROC) Curve is calculated as a measure of the model's ability to distinguish between positive and negative classes. A higher AUC score indicates a better-performing model.
2. Error_Cost_Score: This custom evaluation metric is specifically designed for this project. It considers the financial impact of false negatives (FN) and false positives (FP). In this project, a FN costs the company 10 times more than a FP. The error_cost_score incorporates these costs into the overall evaluation of the model.

## Libraries Used
The following libraries are used in the implementation of the Loan Application Classification API:
- pandas
- scikit-learn (sklearn)
- imbalanced-learn
- pickle
- FastAPI

The dataset used for this project can be found here: https://www.kaggle.com/competitions/home-credit-default-risk/overview
