import ApproachWindow as AW
import PySimpleGUI as sg
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def detect_column_duplicates(df):
    duplicates = {}  

    columns = df.columns
    num_columns = len(columns)

    for i in range(num_columns - 1):
        for j in range(i + 1, num_columns):
            column1 = columns[i]
            column2 = columns[j]

            if df[column1].dtype == df[column2].dtype:  # Check whether the data types are consistent
                if np.array_equal(df[column1], df[column2]):
                    duplicate_count = df[column1].duplicated().sum()
                    duplicates[f'{column1} - {column2}'] = duplicate_count

    return duplicates

def drawBarChart(value_counts, column,xlabel,ylabel,title,savename,newWindow = False):
    fig, ax = plt.subplots()
    ax.bar(value_counts.index, value_counts.values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.tick_params(axis='x', rotation=45)
    fig.savefig( savename+ '.png')

    if newWindow == True:
        layout = [[sg.Image(filename = savename+ '.png')],
                  [sg.Button('Exit')]]
        window = sg.Window(title, layout)

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Exit':
                break
        window.close()
        os.remove(savename+ '.png')
        return None
    return savename + '.png'


def checkValue(df):
    column_names = df.columns.tolist()

    layout = [
        [sg.Text('Column Name: '), sg.Text(key='-COLUMN-NAME-', size=(15, 1))],
        [[sg.Multiline(size=(40, 15), key='-VALUE-DISTRIBUTION-',disabled = True)],[sg.Image(filename=None,key='-IMAGE-')]],
        [sg.Text('Data Distribution\nChoose column(s) you want to check the range(only for number)')],
        [sg.Checkbox(column_name, key=column_name) for column_name in column_names],
        [sg.Button('Previous'), sg.Button('Next'), sg.Button('Close')],
    ]

    window = sg.Window('Data Viewer', layout)

    current_index = 0

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Close':
            problematic_columns = [column_name for column_name in column_names if window[column_name].get()]
            break

        if event == 'Previous':
            current_index = (current_index - 1) % len(column_names)

        if event == 'Next':
            current_index = (current_index + 1) % len(column_names)

        column_name = column_names[current_index]
        window['-COLUMN-NAME-'].update(column_name)
        value_distribution = df[column_name].value_counts()
        value_counts_str = value_distribution.rename_axis('value').reset_index(name='counts').to_string(index=False)
        window['-VALUE-DISTRIBUTION-'].update(value_counts_str)
        png = drawBarChart(value_distribution, column_name,column_name,'Count',f'{column_name}\'s Count',column_name)
        window['-IMAGE-'].update(filename=png)
        os.remove(png)

    window.close()

    print("Selected Columns:", problematic_columns)
    return problematic_columns

def rangeCheck(df,colName):
    if df.dtypes == 'int64':
        df = df.to_frame()
        layout = [
            [sg.Text(colName)],
            [sg.Text(f"Total length: {len(df)}")],
            [sg.Text('lower limit:'), sg.Spin(values=list(range(101)), initial_value=0, key='-LOWER-')],
            [sg.Text('upper limit:'), sg.Spin(values=list(range(101)), initial_value=100, key='-UPPER-')],
            [sg.Button('Check'), sg.Button('Exit')]
        ]

        window = sg.Window(f"Check {colName} data range", layout,size=(400, 200))


        while True:
            event, values = window.read()
    
            if event == 'Check':
                lower_limit = int(values['-LOWER-'])
                upper_limit = int(values['-UPPER-'])
                count = ((df >= lower_limit) & (df <= upper_limit)).sum().sum()
                sg.popup(f'The number of elements in the specified range is: {count}')
    
            elif event == 'Exit' or event == sg.WINDOW_CLOSED:
                break

        window.close()
        return count / len(df) *100
    else:
        return None

def findMissMatchingItems(file_path, df, column_name):
    if file_path == None:
        return None
    try:
        with open(file_path, 'r') as file:
            text_content = file.read()
    except:
        sg.popup('No such file')
        return None
    non_matching_items = df.loc[~df[column_name].isin(text_content.split())]
    #print(non_matching_items)
    l = len(df)
    ml = len(non_matching_items)
    layout = [
        [sg.Text('Comparison table')],
        [sg.Multiline(default_text=text_content, size=(50, 10), key='-TEXT-')],
        [sg.Text('Mismatching rows')],
        [sg.Text(f'Missmatching rows / Total rows\n{ml}/{l}')],
        [sg.Table(values=non_matching_items.values.tolist(),
                  headings=non_matching_items.columns.tolist(),
                  max_col_width=25,
                  auto_size_columns=True,
                  justification='left',
                  num_rows=min(10, len(non_matching_items)))]
    ]

    window = sg.Window('find Miss Matching Items', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

    window.close()
    return {f'match rate {column_name}': (1 - ml/l) * 100}

class ConAp(AW.ApWindow):
    def __init__(self,list,filename,windowName,N = 0,additionalfile = None,help_word = ''):
        super().__init__(list,filename,windowName,N,additionalfile,help_word)
    
    def Uniqueness(self,data):
        length = len(data)
        unique = data.duplicated().mean() * 100
        if length >1000:
            return 100 - round((unique) * (1000 / length),2)
        else:
            return round(100- unique,2)

    def approaches(self,select_approaches):
        if len(self.score) != 0:
            self.score = dict()
            self.otherOut = []

        root = os.getcwd()
        path = root + "\\NewApproach\\Consistency\\"
        for i in select_approaches:
            if i.find(".py") != -1:
                try:
                    sg.popup(f"{i} Start")
                    temp = open(path + i).read()
                    exec(temp)
                except:
                    print(f'Approach {i} fail')
            elif i == "Uniqueness":

                sg.popup("Uniqueness Start")
                #check the dataset (not include addtionial dataset)
                columns = self.data.columns.tolist()
                columns.append('Auto')
                Uniq = AW.clickWindow(columns,"Choose key(s) for Uniqueness check")
                keys = Uniq.showWindow()
                if keys == None:
                    continue
                if 'Auto' in keys:
                    max_score = -1
                    for i in self.data.columns.tolist():
                        col_score = self.Uniqueness(self.data[i])
                        if col_score>max_score:
                            max_score=col_score
                            max_col=i
                        if  col_score!= 100:
                            self.otherOut.append(f'column {i} have {round(100 - col_score,2)}% duplicate')
                        else:
                            self.otherOut.append(f'column {i} have no duplicate. It might be a key')
                    self.otherOut.append(f'The least repetitive columns are {max_col}.\nThe repetition rate is {round(100 - max_score,2)}%')
                    subdata = self.data[self.data.columns.tolist()]
                    tempDict = {"Uniqueness":self.Uniqueness(subdata)}
                    self.score.update(tempDict)
                    continue

                subdata = self.data[keys]
                col_score = self.Uniqueness(subdata)
                tempDict = {"Uniqueness":col_score}
                self.score.update(tempDict)
                self.otherOut.append(f'Uniqueness of {keys} is {col_score}%')

            elif i == "Redundancy":
                sg.popup("Redundancy Start")
                #only check the head if there any redundancy between two dataset
                try: 
                    len(self.adddata)
                except:
                    temp = self.addData()
                    if temp == None:
                        continue

                head = set(self.data.columns.tolist()) & set(self.adddata.columns.tolist())
                cw = AW.clickWindow(head,"Choose head that they may have Redundancy")
                text = cw.showWindow()
                if text == None:
                    continue
                count = 0
                for i in text:
                    if self.data[i].isin(self.adddata[i]).any():
                        count += 1
                tempDict = {"Redundancy":round((1 - (count/len(set(self.data.columns.tolist())))) * 100,2)}
                self.score.update(tempDict)
            elif i == "Format":
                sg.popup("Format Start")
                f = AW.FileSelection("Select your comparison table")
                col = AW.clickWindow(self.data.columns,"Select the column you want to check","Select the column you want to check")
                colList = col.showWindow()
                if colList == None:
                    continue
                for i in colList:
                    NewDict = findMissMatchingItems(f.showWindow(),self.data[[i]],i)
                    if NewDict != None:
                        self.score.update(NewDict)
            elif i == "Consistency":
                try: 
                    len(self.adddata)
                    flag = True
                except:
                    temp = self.addData()
                    if temp != None:
                        flag = True
                    else:
                        flag = False

                if flag == True:

                    quickCheck = ""
                    quickCheck += "shape check(check two data you give have same shape or not): " + str(self.data.shape == self.adddata.shape) + "\n"
                    quickCheck += "Common colname: " + str(set(self.data.columns.to_list()) & set(self.adddata.columns.to_list())) + "\n"
                    quickCheck += "Differ colname: " + str(set(self.data.columns.to_list()) ^ set(self.adddata.columns.to_list())) + "\n"
                    sg.popup(quickCheck)

                    cw = AW.clickWindow(["Semantic","Compare Value","Value distribution"],"Choose Type of Consistency you may need to check ","Choose Type of Consistency you may need to check ")
                    Type = cw.showWindow()
                    for i in Type:
                        if i == "Semantic":
                            sg.popup("Semantic start")
                            #ValueTypeCW = AW.clickWindow()
                            inferred_type = []
                            for column_name in self.data.columns:
                                column_data = self.data[column_name]
                                inferred_type.append(pd.api.types.infer_dtype(column_data))
                            Semantic = AW.clickWindow(inferred_type,"Which one(or some) of these types doesn't make sense?",otherText = "Their column names are \n" + self.data.head(2).to_string(index=False))
                            unSemantic = Semantic.showWindow()
                            if unSemantic == None:
                                continue
                            newDict = {"Semantic":(1 - len(unSemantic)/len(self.data.columns))*100}
                            self.score.update(newDict)
        
                        elif i == "Compare Value":

                            sg.popup("Compare Value start")
                            valueCheck = AW.RadioGroupsWindow("Select two columns of data to check whether their values are the same.",self.data.columns.to_list(),self.adddata.columns.to_list(),self.data,self.adddata)
                            ValueScore = valueCheck.showWindow()
                            if ValueScore == None:
                                continue
                            self.score.update(ValueScore)

                        elif i == "Value distribution":
                            sg.popup("Value distribution start")
                            problematic_columns = checkValue(self.data)
                            RS = dict()
                            if len(problematic_columns) == 0:
                                continue
                            for i in problematic_columns:
                                print(i)
                                rangeScore = rangeCheck(self.data[i],i)
                                if rangeScore != None:
                                    newDict = {i:rangeScore}
                                    RS.update(newDict)
                            if len(self.data) > 1000:
                                rangeScoreAvg = sum(RS.values())/len(RS) * (1000 / len(self.data))
                            else:
                                rangeScoreAvg = sum(RS.values())/len(RS)
                            newDict = {"rangeScoreAvg":rangeScoreAvg}
                            RS.update(newDict)
                            self.score.update(RS)
        return 0

