import ApproachWindow as AW
import PySimpleGUI as sg
import pandas as pd
import os

def detectTimeColumns(df):
    all_columns = df.columns
    time_columns_info = {}
    time_columns = []
    for column in all_columns:
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            time_columns.append(column)
            start_time = df[column].min()
            end_time = df[column].max()
            time_columns_info[column] = {'Start Time': start_time, 'End Time': end_time}
    text = ""
    for column, info in time_columns_info.items():
        text += f" {column}\'s start time is: {info['Start Time']}\n"
        text += f" {column}\'s end time is: {info['End Time']}\n"
    return text,time_columns

def averageInterval(df, column):
    time_diff = df[column].sort_values(column).diff()
    max_interval = " ".join(str(time_diff.max()).split()[0:3])
    min_interval = " ".join(str(time_diff.min()).split()[0:3])
    mean_interval = " ".join(str(time_diff.mean()).split()[0:3])
    return f"The maximum interval for updating data is {max_interval}\nThe minimum interval is {min_interval}\nThe average interval is {mean_interval}\n"

class TimelAp(AW.ApWindow):
    def __init__(self,list,filename,windowName,N = 0,additionalfile = None,help_word = ''):
        super().__init__(list,filename,windowName,N,additionalfile,help_word)

    def approaches(self,select_approaches):
        root = os.getcwd()
        path = root + "\\NewApproach\\Timeliness\\"
        for i in select_approaches:
            if i.find(".py") != -1:
                try:
                    sg.popup(f"{i} Start")
                    temp = open(path + i).read()
                    exec(temp)
                except:
                    print(f'Approach {i} fail')
            if i == "General":
                time_text,time_columns = detectTimeColumns(self.data)
                Q = AW.QuestionWindow(time_text + "Is this data still within the validity period?")
                self.otherOut.append(time_text)
                newDict = {"Validity":Q.showWindow()*100}
                self.score.update(newDict)
                AvgInterval = averageInterval(self.data,time_columns)
                Q.changeQuestion(AvgInterval+"Does this update frequency meet your data timeliness requirements?")
                self.otherOut.append(AvgInterval)
                newDict = {"Frequency":Q.showWindow()*100}
                self.score.update(newDict)
                
