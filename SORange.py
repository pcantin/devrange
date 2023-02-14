import pandas as pd
import matplotlib.pyplot as plt
from json import JSONEncoder,dumps
import os

class DevStats:
    TotAnsw = 0
    BEData = {"Not Web":0,"Front End":0,"Front End Only":0,"Back End":0,"Back End Only":0,"Full Stack":0}
    BETech = {"JavaScript":0,"PHP":0,"Ruby":0,"Java":0,"C#":0,"Python":0}#,"Other":0}
    BETechEdge = {}
    BEShape = {}

    tmpShapeData = [{},{},{},{},{},{},{}]

    def __init__(self, TotAnsw):
        self.TotAnsw = TotAnsw
        self.BEData = {"Not Web":0,"Front End":0,"Front End Only":0,"Back End":0,"Back End Only":0,"Full Stack":0}
        self.BETech = {"JavaScript":0,"PHP":0,"Ruby":0,"Java":0,"C#":0,"Python":0}#,"Other":0}
        self.BETechEdge = {}
        self.BEShape = {}

    def serialise(self, fName: str):
        dataStr = dumps(self, indent=4, cls=DevStatsEncoder)
        pathStr = os.getcwd() + "/data/"
        if not os.path.isdir(pathStr):
            os.mkdir(pathStr)
        file = open(pathStr + fName, "w")
        file.write(dataStr)
        file.close()

    def extractData(self, fileVar, FrtEnd, BETechs):
        tmpBETech = set([])
        for stack in BETechs.items():
            tmpBETech = tmpBETech.union(stack[1])

        for index, rowVal in fileVar.iterrows():
            FETot = len(set(list(str(rowVal['WebframeHaveWorkedWith']).split(';'))) & FrtEnd)
            BETot = len(set(list(str(rowVal['WebframeHaveWorkedWith']).split(';'))) & tmpBETech)
            devShape = []

            if FETot <= 0 and BETot <= 0:
                self.BEData["Not Web"] += 1

            if FETot > 0:
                self.BEData["Front End"] += 1
                if BETot > 0:
                    self.BEData["Full Stack"] += 1
                else:
                    self.BEData["Front End Only"] += 1

            if BETot > 0:
                self.BEData["Back End"] += 1
                if FETot == 0:
                    self.BEData["Back End Only"] += 1

                for techId, techVal in BETechs.items():
                    BELang = 1 if techId in list(str(rowVal['LanguageHaveWorkedWith']).split(';')) else 0
                    if BELang == 0:
                        BELang = len(set(list(str(rowVal['LanguageHaveWorkedWith']).split(';'))) & techVal)

                    BEfrmw = len(set(list(str(rowVal['WebframeHaveWorkedWith']).split(';'))) & techVal)
                    if BELang > 0 and BEfrmw > 0:
                        devShape.append(techId)
                        self.BETech[techId] += 1

                shapeStr = ','.join(devShape)
                id = len(devShape) - 1
                if id >= 0:
                    if shapeStr in self.tmpShapeData[id]:
                        self.tmpShapeData[id][shapeStr] += 1
                    else:
                        self.tmpShapeData[id][shapeStr] = 0

        for key, value in enumerate(self.tmpShapeData):
            self.BEShape[str(key + 1)] = sum(value.values())

        for techId1 in range(0, len(BETechs)):
            for techId2 in range(techId1 + 1, len(BETechs)):
                for value in self.tmpShapeData:
                    for shpId, shpVal in value.items():
                        if list(BETechs)[techId1] in shpId and list(BETechs)[techId2] in shpId:
                            if str(list(BETechs)[techId1] + " + " + list(BETechs)[techId2]) in self.BETechEdge:
                                self.BETechEdge[list(BETechs)[techId1] + " + " + list(BETechs)[techId2]] += shpVal
                            else:
                                self.BETechEdge[list(BETechs)[techId1] + " + " + list(BETechs)[techId2]] = shpVal


    def sortData(self):
        self.BETech = dict(sorted(self.BETech.items(), key=lambda item: item[1], reverse=True))
        self.BEData = dict(sorted(self.BEData.items(), key=lambda item: item[1], reverse=True))

        for index, val in enumerate(self.tmpShapeData):
            self.tmpShapeData[index] = dict(sorted(val.items(), key=lambda item: item[1], reverse=True))

        self.BETechEdge = dict(sorted(self.BETechEdge.items(), key=lambda item: item[1], reverse=True))

    def asPercent(self):
        for key, value in self.BEData.items():
            self.BEData[key] = round((value / self.TotAnsw) * 100, 2)

        totItem = sum(self.BETech.values())
        for key, value in self.BETech.items():
            self.BETech[key] = round((value / totItem) * 100, 2)

        totItem = sum(self.BETechEdge.values())
        for key, value in self.BETechEdge.items():
            self.BETechEdge[key] = round((value / totItem) * 100, 2)

        totItem = sum(self.BEShape.values())
        for key, value in self.BEShape.items():
            self.BEShape[key] = round((value / totItem) * 100, 2)

    def graphData(self, dataID):
        match dataID:
            case 1:
                dataV = self.BEData
                gTitle = "Development Types Distribution"
                gXlabel = "Types of development"
                gYlabel = "% of Developers"
                yLim = [0,80]
            case 2:
                dataV = self.BETech
                gTitle = "Backend Stacks Distribution"
                gXlabel = "Backend Stacks"
                gYlabel = "% of Backend Developers"
                yLim = [0,35]
            case 3:
                dataV = self.BETechEdge
                gTitle = "Distribution of Backend Stacks Combinations"
                gXlabel = "Backend Stacks Combinations"
                gYlabel = "% of Backend Dev. with 2+ stacks"
                yLim = [0,50]
            case 4:
                dataV = self.BEShape
                gTitle = "Number of Backend Stacks Mastered"
                gXlabel = "Total Backend Stacks Mastered"
                gYlabel = "% of Backend Developers"
                yLim = [0,90]

        techData = pd.DataFrame.from_dict(dataV, orient='index')
        ax = techData.plot.bar(legend=None)
        i = 0
        for key in dataV.keys():
            plt.text(s=str(dataV[key]) + "%", x=i, y=dataV[key]+0.8, color="k", verticalalignment="bottom", horizontalalignment="center", rotation=90, size=10)
            i += 1

        ax.set_title(gTitle)
        ax.axes.set_xlabel(gXlabel)
        ax.axes.set_ylabel(gYlabel)
        ax.set_ylim(yLim)
        plt.show()


class DevStatsEncoder(JSONEncoder):
    def default(self, object):
        if isinstance(object, DevStats):
            return object.__dict__
        else:
            return JSONEncoder.default(self, object)


def main():
    fileRaw = pd.read_csv('survey_results_public.csv')

    FrtEnd = set(["Angular","Angular.js","Gatsby","jQuery","React.js","Svelte","Vue.js","HTML/CSS","TypeScript"])
    BETechs = {
        "JavaScript":set(["Express","Clojure","Node.js"]),
        "PHP":set(["Drupal","Laravel","Symfony"]),
        "Ruby":set(["Ruby on Rails","Crystal"]),
        "Java":set(["Spring","Groovy","Kotlin"]),
        "C#":set(["ASP.NET","ASP.NET Core","F#"]),
        "Python":set(["Django","FastAPI","Flask"])
#        "Other":set(["Dart","Delphi","Elixir","Erlang","Go","Haskell","Perl","Rust","C","C++","Scala","VBA"]),
    }

    fileVar = fileRaw[fileRaw['MainBranch'] == 'I am a developer by profession']

    dev21 = DevStats(len(fileVar))    
    dev21.extractData(fileVar, FrtEnd, BETechs)
    dev21.sortData()
    dev21.asPercent()
    #dev21.serialise("SO21Range.json")
    dev21.graphData(1)


if __name__ == '__main__':
    main()