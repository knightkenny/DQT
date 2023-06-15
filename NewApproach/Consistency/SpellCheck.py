import nltk
from nltk.corpus import words

nltk.download('words')

df = self.data

word_list = set(words.words())

CW = AW.clickWindow(df.columns.tolist(),'Select name column','Select name column')
NameColumn = CW.showWindow()
NameColumn = NameColumn[0]

misspelled_indexes = []
for index, row in df.iterrows():
    words_in_text = row[NameColumn].lower().split()
    for word in words_in_text:
        if word not in word_list:
            misspelled_indexes.append(index)
            break

misscount = 0
for index in misspelled_indexes:
    if misscount <= 20:
        text = df.loc[index, NameColumn]
        self.otherOut.append(f"Spelling error in text '{text}' at index {index}")
        misscount += 1
if misscount == 21:
    self.otherOut.append(f"There still {len(misspelled_indexes) - 20} doesn\'t display")

self.score.update({'SpellCheck':round((1- len(misspelled_indexes)/len(df))*100,2)})