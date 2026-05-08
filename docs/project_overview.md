# Technical Overview - SmartHire AI
**Author:** Pushkar Sharma

## Objective
The goal of this project is to analyze a dataset of 10,000+ student records and predict internship selection using Machine Learning.

## Methodology
- **Data Preprocessing:** Handled categorical encoding and data type conversion using `tidyverse`.
- **Statistical Testing:** Performed Chi-Square and T-Tests to validate significant predictors.
- **Modeling:** Utilized the `Random Forest` algorithm (via `ranger`) for classification due to its robustness against overfitting.

## Performance
- **Accuracy:** ~90%
- **Evaluation Metrics:** ROC-AUC and Confusion Matrix were used for validation.