import rrdtool
import json
from datetime import datetime
import os
import plotly
from plotly.graph_objs import Scatter, Layout


class CatRRDToCVS():

    pathCurrent = os.getcwd()
    
    def searchInformation(self, information): 
        os.chdir(self.pathCurrent)  
        with open("config/config.json") as json_file:
            data = json.load(json_file)
        json_file.close()

        return data[information]

    def listOfPaths(self):

        mainpath = self.searchInformation("endereco_rrd")
        os.chdir(mainpath)
        # user = os.listdir()
        # os.chdir(user[0])
        titles = os.listdir()
        listPaths = []
        listTitle = []
        listSubtitlePlusPath = []
        listMetrics = []

        for title in titles:
        
            os.chdir(title)
            subtitles = os.listdir()

            for subtitle in subtitles:

                listSubtitlePlusPath.append(subtitle)
                listSubtitlePlusPath.append(mainpath +  "//" + title + "//" + subtitle)
                #  listSubtitlePlusPath.append(mainpath + user[0] + "//" + title + "//" + subtitle)
                listMetrics.append(listSubtitlePlusPath)

                listSubtitlePlusPath = []
            os.chdir("..")
            
            listTitle.append(title)
            listTitle.append(listMetrics)
            listMetrics = []
            listPaths.append(listTitle)
            listTitle = []

        return listPaths
    
    def listOfTitles(self):
 
        dicionary = self.listOfPaths()
        listOfTitle=[]
        os.chdir(self.pathCurrent)
        for i in range(len(dicionary)):
            listOfTitle.append(dicionary[i][0])
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(listOfTitle, f, ensure_ascii=False, indent=2)

    def getPacket(self, path):
        
        list = rrdtool.fetch(path,'AVERAGE', '-a','r 30m','-s ' + self.searchInformation("tempo_inicial"))
        start, end, step = list[0]
        values = list[2]
        return start, end, step, values

    def createHTML(self, dicionary):
        
        for i in range(len(dicionary)):
        
            Title = dicionary[i][0]

            for n in range(len(dicionary[i][1])):  
                subtitle = dicionary[i][1][n][0]
                path = dicionary[i][1][n][1]
                start, end, step, values = self.getPacket(path)

                if n == 0:
                    timelist = []
                    value = []
                    listData = []
        
                    for k in range(len(values)):
                        timelist.append(datetime.fromtimestamp(start + (k*step)))
                        value.append(values[k][0])      #values is tuple

                    axialData = {"type": "scatter",
                    "x": timelist,
                    "y": value,
                    "name":subtitle.replace(".rrd","")}
                    listData.append(axialData)

                else:
                    value = []
                    
                    for k in range(len(values)):
                        value.append(values[k][0])      #values is tuple
                    
                    axialData = {"type": "scatter",
                    "x": timelist,
                    "y": value,
                    "name":subtitle.replace(".rrd","")}
                    listData.append(axialData)
                   
                    
            os.chdir(self.searchInformation("endereco_data"))
            
            plotly.offline.plot(
                {
                "data": listData,
                "layout": Layout(title=Title)
                 },
                filename = Title +".html"
            )            
            
classblabla = CatRRDToCVS()
lista = classblabla.listOfPaths()
classblabla.createHTML(lista)
classblabla.listOfTitles()
print("Arquivos atualizados :D")
