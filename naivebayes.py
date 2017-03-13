import pandas as pd
import csv
import math
'''Big 5 persoality Traits:
    1. Openness
    2. Conscientiousness
    3. Extraversion
    4. Agreeableness
    5. Neuroticism
 '''
class NaiveBayes: #Classification algorithm for personality identification based on big 5 traits
    oStatus = []
    cStatus = []
    eStatus = []
    aStatus = []
    nStatus = []
    megaStatus = []
    def __init__(self):
        pass
    def train(self,file):
        with open(file, 'r',encoding='utf-8',errors='replace') as f:
            reader = csv.DictReader(f)
            #Separate the status according to the personality and also create a megaDocument of status
            for row in reader:
                if row['cEXT'] == 'y':
                    self.eStatus.append(row['STATUS'])
                if row['cNEU'] == 'y':
                    self.nStatus.append(row['STATUS'])
                if row['cAGR'] == 'y':
                    self.aStatus.append(row['STATUS'])
                if row['cCON'] == 'y' :
                    self.cStatus.append(row['STATUS'])
                if row['cOPN'] == 'y' :
                    self.oStatus.append(row['STATUS'])
                self.megaStatus.append(row['STATUS'])
            #Calculate the prior probabilty of each class
        priorofE,priorofN,priorofA,priorofC,priorofO = self.calculatePrior(self.eStatus,self.nStatus,self.aStatus,self.cStatus,self.oStatus,self.megaStatus)
        print("\n Openness: %f\n Conscientiousness: %f\n Extraversion: %f\n Agreeableness: %f\n Neuroticism: %f\n" %(priorofO,priorofC,priorofE,priorofA,priorofN))
        #Calculate likelihood
        #Using Hash Table
        hTable = self.generateHash(self.eStatus,self.nStatus,self.aStatus,self.cStatus,self.oStatus) 
        print(pd.DataFrame(hTable))
        #status = ((self.megaStatus[0])).split()
        #print(len(status))
    def calculatePrior(self,eStatus,nStatus,aStatus,cStatus,oStatus,megaStatus):
       total = len(megaStatus)
       priorofE = len(eStatus)/total
       priorofN = len(nStatus)/total
       priorofA = len(aStatus)/total
       priorofC = len(cStatus)/total
       priorofO = len(oStatus)/total
       return priorofE,priorofN,priorofA,priorofC,priorofO
   
    def generateHash(self,eStatus,nStatus,aStatus,cStatus,oStatus):
       eStatusList = []
       nStatusList = []
       aStatusList = []
       cStatusList = []
       oStatusList = []
       eStatusDict = {}
       nStatusDict = {}
       aStatusDict = {}
       cStatusDict = {}
       oStatusDict = {}
       #Split status into each word
       for i in eStatus:
           eStatusList.extend(i.split())
       for i in nStatus:
           nStatusList.extend(i.split())
       for i in aStatus:
           aStatusList.extend(i.split())
       for i in cStatus:
           cStatusList.extend(i.split())
       for i in oStatus:
           oStatusList.extend(i.split())
       #Set each splitted word as an attribute and calculate their frequency
       for i in eStatusList[0:100]:
           eStatusDict[i] = eStatusList.count(i)
       for i in nStatusList[0:100]:
           nStatusDict[i] = nStatusList.count(i)
       for i in aStatusList[0:100]:
           aStatusDict[i] = aStatusList.count(i)
       for i in cStatusList[0:100]:
           cStatusDict[i] = cStatusList.count(i)
       for i in oStatusList[0:100]:
           oStatusDict[i] = oStatusList.count(i)
       #Adjust Valuse: To those attributes present in one class but not in other as if they are left zero doesn't work well
       eStatusDict,nStatusDict,aStatusDict,cStatusDict = self.adjustValue(oStatusDict,eStatusDict,nStatusDict,aStatusDict,cStatusDict) 
       eStatusDict,nStatusDict,aStatusDict,oStatusDict = self.adjustValue(cStatusDict,eStatusDict,nStatusDict,aStatusDict,oStatusDict) 
       eStatusDict,nStatusDict,oStatusDict,cStatusDict = self.adjustValue(aStatusDict,eStatusDict,nStatusDict,oStatusDict,cStatusDict) 
       eStatusDict,oStatusDict,aStatusDict,cStatusDict = self.adjustValue(nStatusDict,eStatusDict,oStatusDict,aStatusDict,cStatusDict)
       oStatusDict,nStatusDict,aStatusDict,cStatusDict = self.adjustValue(eStatusDict,oStatusDict,nStatusDict,aStatusDict,cStatusDict) 
       #Generate a likelihood probability
       for key,value in eStatusDict.items():
           eStatusDict[key] = value/len(eStatusList)
       for key,value in nStatusDict.items():
           nStatusDict[key] = value/len(nStatusList)
       for key,value in aStatusDict.items():
           aStatusDict[key] = value/len(aStatusList)
       for key,value in cStatusDict.items():
           cStatusDict[key] = value/len(cStatusList)
       for key,value in oStatusDict.items():
           oStatusDict[key] = value/len(oStatusList)
       hTable = {'Extraversion':eStatusDict,'Neuroticism':nStatusDict,'Agreebleness':aStatusDict,'Conscientiousness':cStatusDict,'Openness':oStatusDict}
       return hTable
    def adjustValue(self,dict0,dict1,dict2,dict3,dict4):
       for i in dict0:
           if i not in dict1:
               dict1[i] = 0
           if i not in dict2:
               dict2[i] = 0
           if i not in dict3:
               dict3[i] = 0
           if i not in dict4:
               dict4[i] = 0
       return dict1,dict2,dict3,dict4

    def caclulate():
       pass
   
    def classify():
       pass

    def test():
       pass
if __name__=="__main__":
    try:
        naivebayes = NaiveBayes()
        naivebayes.train('dataSet/mypersonality_final/mypersonality_final.csv')
    except FileNotFoundError:
        print("Training file unavailable")

