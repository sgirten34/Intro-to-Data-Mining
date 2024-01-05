library(tidyverse)
library(arulesSequences)
library(arules)

setwd("~/Masters/Intro to Data Mining/A2 Text Mining Contiguous Sequential Patterns")

#seq_ID = 1:10000
#write.table(sequenceID, "sequenceID.txt", row.names = F)

reviews = read_lines("reviews_sample.txt")


reviews2 = tibble(sequenceID = 1:10000,
                  items = str_split(reviews, " ")) %>% 
  unnest_longer(items) %>% 
  group_by(sequenceID) %>% 
  mutate(eventID = row_number()) %>% 
  ungroup() %>% 
  relocate(sequenceID, eventID)

# Make sequenceID, eventID and items into factors 
reviews2 = data.frame(lapply(reviews2, as.factor))

write.table(reviews2, 'reviews_sample2.txt', sep = " ", col.names = F, row.names = F, quote = F)
transact = read_baskets('reviews_sample2.txt', sep = ' ', info = c("sequenceID","eventID"))
seq = cspade(transact, parameter = list(support = 0.01, 
                                        maxsize = NULL, 
                                        maxlen = NULL,
                                        mingap = 1,  # set mingap/maxgap to 1 in order to get contiguous sequential patterns
                                        maxgap = 1),
             control = list(verbose = T))
df_seq = as(seq, "data.frame")

sup = support(seq, transactions = transact, type = 'absolute')

df_seq2 = df_seq %>% 
  bind_cols(sup) %>% 
  rename(abs_sup = 3)

# This version of absolute support counted multiple instances of the same sequence for one event
# df_out = df_seq2 %>% 
#   mutate(sequence2 = str_remove_all(sequence, "[{}<>]")) %>% 
#   mutate(sequence3 = str_replace_all(sequence2, ",", ";")) %>% 
#   mutate(seq_final = str_c(abs_sup, ":", sequence3)) %>% 
#   select(seq_final)

df_out2 = df_seq2 %>% 
  mutate(sequence2 = str_remove_all(sequence, "[{}<>]")) %>% 
  mutate(sequence3 = str_replace_all(sequence2, ",", ";")) %>% 
  mutate(seq_final = str_c(support * 10000, ":", sequence3)) %>% 
  select(seq_final)


write_delim(df_out2, "patterns.txt", delim = "", col_names = F)
  
#transactions = read_baskets('reviews_sample.txt', sep = ' ', info = c("sequenceID","eventID"))
# transact = as(reviews2, "transactions")
# transactionInfo(transact)$sequenceID = reviews2$sequenceID
# transactionInfo(transact)$eventID = reviews2$eventID
# inspect(head(transact))
# summary(transact)
# seq = cspade(transact, parameter = list(support = 0.01, maxsize = NULL, maxlen = NULL), control = list(verbose = T))



# create transaction object with a sequence ID
#df.trans = as(revs, "transactions")
#transactionInfo(df.trans)$sequenceID = revs$sequenceID
#inspect(head(df.trans))

# Sort by sequence ID
#df.trans = df.trans[order(transactionInfo(df.trans)$sequenceID)]
#seq = cspade(df.trans, parameter = list(support = 0.01))


#write.table(reviews3, 'reviews_sample2.txt', sep = " ", col.names = F, row.names = F, quote = F)

#transactions = read_baskets('reviews_sample.txt', sep = ' ', info = c("sequenceID","eventID"))
#transact = as(transactions, "transactions")

#summary(transactions)
#hd = head(DATAFRAME(transactions))

#freq_seq = cspade(transactions, parameter = list(support = 0.01))
