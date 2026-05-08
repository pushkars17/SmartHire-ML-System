library(tidymodels)
library(vip)

model <- readRDS("output/models/selection_model.rds")
test_data <- readRDS("data/processed/test_data.rds")

# Predictions
results <- test_data %>%
  bind_cols(predict(model, test_data))

# Metrics
metrics_res <- metrics(results, truth = selected, estimate = .pred_class)
write.csv(metrics_res, "output/model_performance.csv")

# Feature Importance Plot
p3 <- model %>% extract_fit_engine() %>% vip() + theme_minimal()
ggsave("output/plots/feature_importance.png", p3)

print("Evaluation complete. Check 'output' folder.")