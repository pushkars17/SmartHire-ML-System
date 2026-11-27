library(tidyverse)

# Raw data load karein
raw_df <- read.csv("data/raw/Internship_Selection_Dataset.csv")

# Advance Processing
clean_df <- raw_df %>%
  mutate(across(c(selected, college_tier, placement_training, extracurricular), as.factor)) %>%
  mutate(cgpa_category = case_when(
    CGPA >= 9 ~ "Elite",
    CGPA >= 7.5 ~ "High",
    TRUE ~ "Average"
  )) %>%
  drop_na()

saveRDS(clean_df, "data/processed/clean_data.rds")
print("Data cleaning done and saved in data/processed/")