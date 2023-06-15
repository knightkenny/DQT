import ApproachWindow as AW
import os

class UniAp(AW.ApWindow):
    def __init__(self,list,filename,windowName,N = 0,additionalfile = None,help_word = ''):
        super().__init__(list,filename,windowName,N,additionalfile,help_word)

    def approaches(self,select_approaches):
        root = os.getcwd()
        path = root + "\\NewApproach\\Others\\"
        for i in select_approaches:
            if i.find(".py") != -1:
                try:
                    sg.popup(f"{i} Start")
                    temp = open(path + i).read()
                    exec(temp)
                except:
                    print(f'Approach {i} fail')
            if i == "test":
                continue

