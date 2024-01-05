library(tidyverse)
library(tidymodels)

setwd("~/Masters/Intro to Data Mining/A3 K Means Clustering")

data = read_delim("places.txt", delim = ",", col_names = c("Longitude", "Latitude"))

# online example at https://www.tidymodels.org/learn/statistics/k-means/

kclust = kmeans(data, centers = 3)
summary(kclust)

output = augment(kclust, data) %>% 
  mutate(id = row_number() - 1) %>% 
  rename(cluster_id = .cluster) %>% 
  mutate(cluster_id = as.numeric(cluster_id)) %>% 
  mutate(cluster_id = cluster_id -1) %>% 
  mutate(output_final = str_c(id, " ", cluster_id))

output_final = as.tibble(output$output_final)

write_delim(output_final, "clusters.txt", delim = "", col_names = F)
