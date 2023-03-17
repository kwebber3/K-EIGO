library(tidyverse)
library(readxl)

x = read_excel("Book1.xlsx")

x = read_excel("Book2.xlsx") %>%
  group_by(`Vocab-expression`) %>%
  summarise(`Opt-Voc-Index` = mean(`Opt-Voc-Index`)) %>%
  right_join(x)
  

x %>%
  mutate(Japanese = `Vocab-kana`) %>%
  group_by(`Japanese`) %>%
  summarise(English = paste(`Vocab-meaning`, collapse = "@"),
            `Japanese Example` = paste(`Sentence-kana`, collapse = "@"),
            `English Sentence` =  paste(`Sentence-meaning`, collapse = "@"),
            index = mean(`Opt-Voc-Index`, na.rm = TRUE)) %>%
  arrange(index) %>%
  select(-index) %>%
  mutate(`listening score` = 0, `speaking score` = 0) %>%
  write_tsv("Listening_Speaking.txt")

x %>%
  mutate(Kanji = `Vocab-expression`) %>%
  group_by(`Kanji`) %>%
  summarise(English = paste(`Vocab-meaning`, collapse = "@"),
            Reading = paste(`Vocab-kana`, collapse = "@"),
            `Example Sentence` = paste(`Sentence-expression`, collapse = "@"),
            `Example Sentence Reading` = paste(`Sentence-kana`, collapse = "@"),
            `English Sentence` =  paste(`Sentence-meaning`, collapse = "@"),
            index = mean(`Opt-Voc-Index`, na.rm = TRUE)) %>%
  arrange(index) %>%
  select(-index) %>%
  mutate(`reading score` = 0, `writing score` = 0) %>%
  write_tsv("Reading_Writing.txt")
