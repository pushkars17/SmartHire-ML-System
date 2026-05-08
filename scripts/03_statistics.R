# ==========================================
# Script Name: 03_statistics.R
# Purpose: Statistical Analysis & Hypothesis Testing
# Author: Pushkar Sharma
# ==========================================

library(tidyverse)
library(corrplot)

# 1. Processed data load karein
df <- readRDS("data/processed/clean_data.rds")

# 2. Correlation Matrix (Numerical variables ke beech rishta)
# Isse pata chalega ki kaunse scores ek doosre se jude hain
numeric_cols <- df %>% select_if(is.numeric) %>% select(-student_id)
cor_matrix <- cor(numeric_cols)

# Correlation Heatmap ko save karein
png("output/plots/correlation_heatmap.png", width=800, height=800)
corrplot(cor_matrix, method="color", type="upper", 
         addCoef.col = "black", # Numbers dikhane ke liye
         tl.col="black", tl.srt=45, 
         title="\n\n Statistical Correlation of Candidate Features",
         mar=c(0,0,1,0))
dev.off()

# 3. Hypothesis Testing: College Tier vs Selection
# Sawal: Kya Tier 1 aur Tier 3 ke students ki selection rate mein significant difference hai?
tier_table <- table(df$college_tier, df$selected)
chi_test <- chisq.test(tier_table)

# Test results ko ek text file mein save karein
sink("output/statistical_tests_report.txt")
print("--- Chi-Square Test: College Tier vs Selection ---")
print(chi_test)
print("Interpretation: Agar p-value < 0.05 hai, toh College Tier ka selection par asar padta hai.")

# 4. T-Test: Coding Score vs Selection
# Sawal: Kya selected candidates ka coding score non-selected se significantly zyada hai?
t_test_result <- t.test(coding_test_score ~ selected, data = df)
print("\n--- T-Test: Coding Score vs Selection Status ---")
print(t_test_result)
sink()

# 5. Visualization: Score Distribution by Selection
p_stats <- ggplot(df, aes(x=selected, y=coding_test_score, fill=selected)) +
  geom_violin(trim=FALSE) +
  geom_boxplot(width=0.1, fill="white") +
  theme_minimal() +
  labs(title="Coding Score Distribution: Selected vs Rejected",
       subtitle="Statistical spread of technical scores",
       x="Selected (0=No, 1=Yes)", y="Coding Test Score")

ggsave("output/plots/statistical_distribution.png", p_stats)

print("Step 03: Statistical Analysis Complete. Report saved in output/ folder.")