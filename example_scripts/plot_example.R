library(tidyverse)

sensor_data_clean <- sensor_data %>% 
  mutate(timestamp = floor_date(timestamp, unit = "seconds")) %>%
  pivot_longer(-timestamp, names_to = "sensor", values_to = "value", values_transform = as.integer) %>%
  drop_na(value) %>%
  arrange(timestamp)

sensor_data_clean %>%
  ggplot(aes(x = timestamp, y = value, color = sensor)) +
  geom_line()