import ApproachWindow as AW
import PySimpleGUI as sg
import pandas as pd
import os

class CpltAp(AW.ApWindow):
    def __init__(self,list,filename,windowName,N = 0,additionalfile = None,help_word = ''):
        super().__init__(list,filename,windowName,N,additionalfile,help_word)

    def approaches(self,select_approaches):
        root = os.getcwd()
        path = root + "\\NewApproach\\Completeness\\"
        for i in select_approaches:
            if i.find(".py") != -1:
                try:
                    sg.popup(f"{i} Start")
                    temp = open(path + i).read()
                    exec(temp)
                except:
                    print(f'Approach {i} fail')
            if i == "Mandatory":
                sg.popup("Mandatory Completeness Start")
                pd.set_option('display.max_columns', 30)
                MA = AW.clickWindow(self.data.columns,"Choose your Mandatory Attributes", str(self.data.head(3)))
                MAcol = MA.showWindow()
                if MAcol == None:
                    continue
                missingValuesCount = dict()
                for i in MAcol:
                    newDict = {"M " +i:self.data[i].isna().sum().sum()}
                    missingValuesCount.update(newDict)
                self.score.update(missingValuesCount)
                sg.popup("Mandatory Completeness finish")
            if i == "Optional":
                sg.popup("Optional Completeness Start. Try check less columns or the result plot will be hard to check")
                OA = AW.clickWindow(self.data.columns,"Choose your Optional Attributes", str(self.data.head(3)))
                OAcol = OA.showWindow()
                missingValuesCount = dict()
                for i in MAcol:
                    newDict = {"O " + i:self.data[i].isna().sum().sum()}
                    missingValuesCount.update(newDict)
                self.score.update(missingValuesCount)
                sg.popup("Optional Completeness finish")             
            if i == "Auto":
                missingValuesCount = dict()
                for i in self.data.columns:
                    newDict = {i:self.data[i].isna().sum().sum()}
                    missingValuesCount.update(newDict)
                self.score.update(missingValuesCount)
                 