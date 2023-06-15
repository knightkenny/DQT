df = self.data

name_columns = [col for col in df.columns if 'name' in col]

if len(name_columns)== 1:
    Q = AW.QuestionWindow(f'Does this column contain the user\'s name?\n{df[name_columns].head(3)}')
    if Q.showWindow() == 1:
        NameColumn = name_columns[0]
elif len(name_columns) > 1:
    CW = AW.clickWindow(name_columns.tolist(),'Select name column','Select name column')
    NameColumn = CW.showWindow()
else:
    CW = AW.clickWindow(df.columns.tolist(),'Select name column','Select name column')
    NameColumn = CW.showWindow()

if df[NameColumn].squeeze().dtype == 'object':

    abbreviation_count = df[df[NameColumn].squeeze().str.contains(r'\b[A-Z]\.')].shape[0]
    full_name_count = df[~df[NameColumn].squeeze().str.contains(r'\b[A-Z]\.')].shape[0]
    self.otherOut.append(f'Full name count: {full_name_count}')
    self.otherOut.append(f'abbreviation count: {abbreviation_count}')
    if full_name_count > abbreviation_count:
        newDict = {'NameSpell':round(full_name_count/len(df)*100,2)}
    else:
        newDict = {'NameSpell':round(abbreviation_count/len(df)*100,2)}
    self.score.update(newDict)