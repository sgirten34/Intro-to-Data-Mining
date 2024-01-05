library(tidyverse)
library(arules)



setwd("~/Masters/Intro to Data Mining/A1 Association Rules Mining")

transactions = read.transactions('categories_2.txt', format = 'basket', sep = ';', quote = "")
#transact = as(transactions, "transactions")

summary(transactions)


# Part One ----------------------------------------------------------------


assoc_rules = apriori(transactions, parameter = list(supp = 0.01, conf = 0, maxlen = 1))# parameter = list(maxlen = 1))
summary(assoc_rules)

inspect(assoc_rules)


transact2 = apriori(transactions, parameter = list(supp = 0.01, target = 'frequent itemsets'))



check_label = itemFrequency(transactions, type = 'absolute')



# Part Two ----------------------------------------------------------------
rules2 = apriori(transactions, parameter = list(supp = 0.01, target = 'frequent itemsets'))
rules2 = DATAFRAME(rules2)

rules2_output = rules2 %>% 
  mutate(itemsets = str_remove_all(items, "[{}]")) %>% 
  mutate(itemsets = str_replace_all(itemsets, ",", ";")) %>% 
  mutate(output = str_c(count, ":", itemsets))

output_final = as_tibble(rules2_output$output)         
write_delim(output_final, "Part 2/patterns.txt", delim = "", col_names = F)
