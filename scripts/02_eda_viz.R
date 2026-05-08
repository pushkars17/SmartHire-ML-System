library(tidyverse)
library(ggthemes)

df <- readRDS("data/processed/clean_data.rds")

# 1. Skill Score vs Coding Score (Selection impact)
p1 <- ggplot(df, aes(x=skills_score, y=coding_test_score, color=selected)) +
  geom_jitter(alpha=0.4) +
  theme_economist() +
  labs(title="Skills vs Coding Score Analysis", subtitle="By Selection Status")

ggsave("output/plots/skills_vs_coding.png", p1)

# 2. College Tier Distribution
p2 <- ggplot(df, aes(x=college_tier, fill=selected)) +
  geom_bar(position="dodge") +
  theme_fivethirtyeight() +
  labs(title="Selection Rate by College Tier")

ggsave("output/plots/tier_distribution.png", p2)