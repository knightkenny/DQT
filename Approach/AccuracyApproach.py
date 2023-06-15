import ApproachWindow as AW
import PySimpleGUI as sg
import os
help = ''

RS = [
      "Is the data sourced from a reliable institution, survey, research, or other reputable sources?",
      "Was the data collected using scientifically sound survey methods, experiments, or other validation techniques?",
      "Does the data have a large sample size, indicating higher representativeness and potentially greater reliability?",
      "Is the data collected recently, reflecting the current situation?",
      "Was any processing or analysis performed on the data after collection?",
      "Does the data provider provide detailed documentation on the data collection and processing methods?",
      "Have quality control measures been implemented to ensure data accuracy?",
      "Does the data provider's institution have a good reputation and credibility as a reliable source of data?"
                ]

RE =[
    "Does the data accurately reflect the real-world events or phenomena it is intended to represent?",
    "Has the data been cross-validated or compared with independent sources to ensure its accuracy?",
    "Is there a documented process in place to verify the accuracy of the data against real-world measurements or observations?",
    "Are there any known errors or discrepancies in the data that could impact its accuracy? (Yes for no errors)",
    "Has the data undergone rigorous quality control measures to ensure its alignment with reality?",
    "Data model is sufficient to represent the real world as required by the organisational need or not?"
    ]
def questionList(list,path = None):
    question = []
    if path == None:
        Q = AW.QuestionWindow("Do you want to read your own questions?")
        if Q.showWindow() == 1:
            R = AW.FileSelection()
            path = R.showWindow()
            try:
                f = open(path)
                for line in f:
                    line = line.strip('\n')
                    question.append(line)
            except:
                print("no such file")
    else:
        f = open(path)
        for line in f:
            line = line.strip('\n')
            question.append(line)
    for i in list:
        question.append(i)

    return question


class AccAp(AW.ApWindow):
    def __init__(self,list,filename,windowName,N = 0,additionalfile = None,help_word = ''):
        super().__init__(list,filename,windowName,N,additionalfile,help_word)

    def approaches(self,select_approaches):
        root = os.getcwd()
        path = root + "\\NewApproach\\Accuracy\\"
        for i in select_approaches:
            if i.find(".py") != -1:
                try:
                    sg.popup(f"{i} Start")
                    temp = open(path + i).read()
                    exec(temp)
                except:
                    print(f'Approach {i} fail')
            elif i == "ReferenceSource":
                sg.popup("Then there are questions about the accuracy of the data sources. The questions are general to fit various types of data sets, and for better results, a customized set of questions for your data set is more accurate.")
                question = questionList(RS)
                RSscore = []
                for q in question:
                    Q = AW.QuestionWindow(q)
                    RSscore.append(Q.showWindow())
                newDict = {"ReferenceSource":round(sum(RSscore)/len(RSscore),2) * 100}
                self.score.update(newDict)
                sg.popup("Reference Source finish")
            elif i == "Reality":
                sg.popup("This function only contains queries about the source of the data. To examine the data in detail, you may need go to Consistency")
                question = questionList(RE)
                REscore = []
                for q in question:
                    Q = AW.QuestionWindow(q)
                    REscore.append(Q.showWindow())
                newDict = {"Reality":round(sum(REscore)/len(REscore),2) * 100}
                self.score.update(newDict)
                sg.popup("Reality finish")
        print(self.score)



