library(tidymodels)

df <- readRDS("data/processed/clean_data.rds")
set.seed(786)

# Data Split
data_split <- initial_split(df, prop = 0.75, strata = selected)
train_data <- training(data_split)
test_data  <- testing(data_split)

# Random Forest Model
rf_spec <- rand_forest(trees = 800) %>%
  set_engine("ranger", importance = "impurity") %>%
  set_mode("classification")

# Recipe (student_id aur cgpa_category ko model se hatana)
rec <- recipe(selected ~ ., data = train_data) %>%
  step_rm(student_id, cgpa_category)

# Workflow aur Training
wf <- workflow() %>% add_recipe(rec) %>% add_model(rf_spec)
final_model <- fit(wf, data = train_data)

saveRDS(final_model, "output/models/selection_model.rds")
saveRDS(test_data, "data/processed/test_data.rds")