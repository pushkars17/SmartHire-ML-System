# SmartHire: AI-Driven Recruitment Prediction System

Developed by: **Pushkar Sharma**

## Overview
SmartHire is an end-to-end Machine Learning project developed in **R** to analyze and predict student internship selections. Using a dataset of 10,000+ records, the system identifies key performance indicators (KPIs) like Coding Scores, CGPA, and Soft Skills that drive successful recruitment.

## Key Features
- **Modular Pipeline:** Separate scripts for Data Cleaning, EDA, Statistics, and Modeling.
- **Advanced Analytics:** Statistical interaction analysis between academic and technical skills.
- **Machine Learning:** Implemented a tuned Random Forest model using the `tidymodels` framework.
- **Automated Visualization:** Generates professional-grade insights automatically in the `output/` folder.

## Project Structure
- `scripts/`: Modular R scripts for the entire data science lifecycle.
- `data/`: Contains raw and processed datasets.
- `output/`: Stores generated plots, trained models, and performance metrics.
- `docs/`: Technical documentation and reports.

## Tech Stack
- **Language:** R
- **Libraries:** Tidyverse, Tidymodels, Ranger, VIP, GGthemes, Corrplot.

## How to Run
1. Place your `Internship_Selection_Dataset.csv` in `data/raw/`.
2. Run `scripts/00_setup.R` to install dependencies.
3. Execute scripts `01` through `05` in numerical order.

## Results
The system achieves over **90% accuracy** in predicting candidate selection, highlighting 'Coding Test Score' and 'Interview Score' as the most significant predictors.