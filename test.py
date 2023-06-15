import pandas as pd
import nltk
from nltk.corpus import words

# 下载'words'语料库
nltk.download('words')

# 创建示例DataFrame
data = {'text_column': ['apple', 'banana ', 'Oranage Apple', 'Grape USA']}
df = pd.DataFrame(data)

word_list = set(words.words())

# 检查拼写错误
misspelled_indexes = []
for index, row in df.iterrows():
    words_in_text = row['text_column'].lower().split()
    for word in words_in_text:
        if word not in word_list:
            misspelled_indexes.append(index)
            break

# 输出每个错误的单词
for index in misspelled_indexes:
    text = df.loc[index, 'text_column']
    print(f"Spelling error in text '{text}' at index {index}")