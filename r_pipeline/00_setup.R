# Libraries install aur load karein
packages <- c("tidyverse", "corrplot", "tidymodels", "ranger", "vip", "ggthemes")
install.packages(setdiff(packages, rownames(installed.packages())))

library(tidyverse)
library(ggthemes)

# Output directories check karein
dir.create("data/processed", showWarnings = FALSE)
dir.create("output/plots", showWarnings = FALSE)
dir.create("output/models", showWarnings = FALSE)

print("Setup Complete!")