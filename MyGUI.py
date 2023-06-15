import PySimpleGUI as sg
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(sys.argv[0]) + '/Approach')

import AccuracyApproach as Acc
import CompletenessApproach as Cplt
import ConsistencyApproach as Cstc
import TimelinessApproach as Timel
import UniquenessApproach as Uni

help_words = [
    'The \'referenceSource\' contains a wide range of questions about data quality, and the results are presented as a percentage.\n\n\'Reality\' encompasses some broad questions about data for the real world, and the results are presented as a percentage.\n\nYou can import your own list of questions, using a txt file, each line contains a question that can be answered with a yes or no answer.',
    'The Completeness section is divided into Mandatory and optional elements, which are treated the same way, only for annotations in the result.\n\n Auto detects all columns, but does not distinguish them.\n\n The result outputs the number of missing values in each column',
    'There are two ways in which the Uniqueness of data can be detected by manually selecting keys. Or with auto, the program detects the uniqueness of each column and gives the columns that may be keys.\n',
    'Timeliness automatically detects the presence of time in the data and calculates its start and end dates as well as the maximum, minimum and average update intervals.',
    'This function is already included in consistency, so there is no method to use it. For adding external programs only.'
    ]

def read_filepath(quickopt = False):
    PATH = os.path.join(os.getcwd(), "lastfilepath.txt")
    if os.path.exists("lastfilepath.txt"):
        filepath = open("lastfilepath.txt")
        temp = []
        for line in filepath:
            line = line.strip('\n')
            if os.path.exists(line) == False:
                filepath.close()
                os.remove(PATH)
                return None
            temp.append(line)

        filepath.close()
        if quickopt == True:
            filepath.close()
            os.remove(PATH)
            return temp

        window = sg.Window("Continue?",[[sg.Text("Open your last dataset?")],[sg.Button("YES"),sg.Button("NO")]])
        while True:
            event,value = window.read()
            if event == "NO":
                window.close()
                filepath.close()
                os.remove(PATH)
                return None

            if event == "YES":
                window.close()
                filepath.close()
                os.remove(PATH)
                return temp
    else:
        print("no file name \"lastfilepath.txt \" ")
        return None

def save_config(filepath):
    fp = open("lastfilepath.txt",mode = "w")
    fp.write(filepath)
    savefolder = os.path.basename(filepath)
    savefolder = savefolder[:savefolder.find(".")]
    if os.path.exists(os.path.dirname(sys.argv[0]) + '\\' + savefolder) == False:
        os.makedirs(os.path.dirname(sys.argv[0]) + '\\' + savefolder)
    fp.close()

def read_approachs():
    root = os.path.dirname(sys.argv[0])
    path = root + "/NewApproach"
    default_approachs = [["ReferenceSource","Reality"],["Mandatory","Optional","Auto"],["Uniqueness","Redundancy","Format","Consistency"],["General"],["test"]]
    
    if os.path.exists(root + "/NewApproach"):
        count = 0
        for i in os.listdir(path):
            if len( os.listdir(path + "/" + i)) >= 1:
                #print(os.listdir(path + "/" + i))
                default_approachs[count] += os.listdir(path + "/" + i)
                #print(default_approachs)
            count += 1
    else:
        os.makedirs(root + "/NewApproach"+"/Accuracy")
        os.makedirs(root + "/NewApproach"+"/Completeness")
        os.makedirs(root + "/NewApproach"+"/Consistency")
        os.makedirs(root + "/NewApproach"+"/Timeliness")
        os.makedirs(root + "/NewApproach"+"/Others")

    return default_approachs
        
class warning_window:
    statement = ""
    def __init__(self, str):
        self.statement = str
        return None

    def display(self):
        window = sg.Window("Warning",[[sg.Text(self.statement,justification = "center")],[sg.Button("Exit")]])
        while True:
            event,value = window.read()
            if event in (None,"Exit"):
                break
        window.close()
        return None

def displayCsvData(file_path):
    df = pd.read_csv(file_path)
    summary = df.describe()
    summary.reset_index(inplace=True)
    summary.rename(columns={'index': ''}, inplace=True)

    layout = [
        [[sg.Text("Summary")],
         [sg.Table(values=summary.values.tolist(),
                  headings=summary.columns.tolist(),
                  max_col_width=25,
                  auto_size_columns=True,
                  justification='left',
                  num_rows=min(10, len(summary)))]],
        [[sg.Text("Dataset")],
         [sg.Table(values=df.values.tolist(),
                  headings=df.columns.tolist(),
                  max_col_width=25,
                  auto_size_columns=True,
                  justification='left',
                  num_rows=min(25, len(df)))]]
    ]

    window = sg.Window('', layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
    window.close()

def main_window(Approach_Names):
    btns = []
    btns.append(sg.Button("General"))
    btns.append(sg.Button("Accuracy"))
    btns.append(sg.Button("Completeness"))
    btns.append(sg.Button("Consistency"))
    btns.append(sg.Button("Timeliness"))
    btns.append(sg.Button("Other"))
    close_btn = sg.Button("Exit")

    selectDB = []
    selectDB.append(sg.Text("Select your Dataset",expand_x = True,justification = "center"))
    selectDB.append(sg.Input(enable_events = True, key = "-IN1-",expand_x = True))
    selectDB.append(sg.FileBrowse("Select Dataset",key = "-DATASET1-",file_types = (("ALL Files","*.csv"),)))
    selectDB.append(sg.Input(enable_events = True, key = "-IN2-",expand_x = True))
    selectDB.append(sg.FileBrowse("Select Additional Dataset(if you need)",key = "-DATASET2-",file_types = (("ALL Files","*.csv"),)))

    layout = [[selectDB],[btns],[close_btn]]

    window = sg.Window("Main page",layout)
    flag_DB = False

    filepath = read_filepath(True)
    while True:
        event,value = window.read(timeout = 100)

        #end the window
        if event in (None,"Exit"):
            break
        #choose dataset
        if event == "-IN1-":
            save_config(value["-IN1-"])
            flag_DB = True

        if (len(value["-IN2-"]) == 0) & (value["-IN2-"] != None):
            value["-IN2-"] = None
        if event == "-IN2-":
            save_config(value["-IN1-"] + "\n" + value["-IN2-"])
        #functions
        if flag_DB == False:
            try:
                #read your last dataset
                if filepath != None :
                    value["-IN1-"] = filepath[0]
                    window["-IN1-"].update(filepath[0])
                    save_config(value["-IN1-"])
                    if len(filepath) == 2:
                        value["-IN2-"] = filepath[1]
                        window["-IN2-"].update(filepath[1])
                    #data = pd.read_csv(filepath[1])# should read when need use, delete this line
                    flag_DB = True
            except:
                print("Failed to read file")
                filepath = None

            if event in ("Accuracy","Completeness","Consistency","Timeliness","Other","General"):
                DBopen =  warning_window ("Select your data first!")
                DBopen.display()

        if flag_DB == True:
            if event == "General":
                displayCsvData(value["-IN1-"])

            if event == "Accuracy":
                ACC = Acc.AccAp(list = Approach_Names[0], N = len(Approach_Names[0]),windowName = "Accuracy",filename = value["-IN1-"],additionalfile = value["-IN2-"],help_word = help_words[0])
                ACC.showWindow()
            if event == "Completeness":
                CPLT = Cplt.CpltAp(list = Approach_Names[1], N = len(Approach_Names[1]),windowName = "Completeness",filename = value["-IN1-"],additionalfile = value["-IN2-"],help_word = help_words[1])
                CPLT.showWindow()
            if event == "Consistency":
                CSTC = Cstc.ConAp(list = Approach_Names[2],N = len(Approach_Names[2]),windowName = "Consistency",filename = value["-IN1-"],additionalfile = value["-IN2-"],help_word = help_words[2])
                CSTC.showWindow()
            if event == "Timeliness":
                TIME = Timel.TimelAp(list = Approach_Names[3], N = len(Approach_Names[3]),windowName = "Timeliness",filename = value["-IN1-"],additionalfile = value["-IN2-"],help_word = help_words[3])
                TIME.showWindow()
            if event == "Other":
                UNI = Uni.UniAp(list = Approach_Names[4],N = len(Approach_Names[4]),windowName = "Other",filename = value["-IN1-"],additionalfile = value["-IN2-"],help_word = help_words[4])
                UNI.showWindow()
    window.close()


main_window(read_approachs())

