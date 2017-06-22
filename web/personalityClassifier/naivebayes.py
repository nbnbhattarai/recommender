import pandas as pd
import dill 
import csv
import math
from nltk.corpus import stopwords
'''Big 5 persoality Traits:
    1. Openness : adventurous, creative
    2. Conscientiousness: organized
    3. Extraversion: excitability, sociability, talkativeness, assertiveness
    4. Agreeableness: trust, kindless, prosocial behavior
    5. Neuroticism: sadness, anxiety, moodiness, emotional.
 '''
class NaiveBayes: #Classification algorithm for personality identification based on big 5 traits
    oStatus = []
    cStatus = []
    eStatus = []
    aStatus = []
    nStatus = []
    megaStatus = []
    stopW = (stopwords.words('english'))
    additionalStop = ['you.', 'you..."',"you've"]
    hashTable = {}
    vSize = 0
    priorofE,priorofN,priorofA,priorofC,priorofO = 0,0,0,0,0
    def __init__(self): #Constructor initializes hashTable and prior probability if it is dumped previously.
        self.stopW += self.additionalStop
        self.stopW = set(self.stopW)
        try:
            with open("hashTable.pik","rb") as f:
                
                print("Hash Table is loaded")
                hTable = dill.load(f)
                self.hTable = hTable
        except FileNotFoundError:
            print("Hash Table is not dumped")
        try:
            with open("prior.pik","rb") as f:
                print("prior probability is loaded")
                prior = dill.load(f)
                self.priorofE,self.priorofN,self.priorofA,self.priorofC,self.priorofO=prior        
        except FileNotFoundError:
            print("Prior Probabaility is not calculated")
        try:
            print("vocabulary size is loaded")
            with open("vocaSize.pik","rb") as f:
                vocaSize = dill.load(f)
                self.vSize = vocaSize
        except FileNotFoundError:
            print("Vocabulary size not computed")
    def filterWords(self,status):
        filteredW = [i for i in status.lower().split() if i not in self.stopW]
        sentence = ""
        for i in filteredW:
            sentence += i
            sentence += " "
        return sentence 
    def train(self,file):
        with open(file, 'r',encoding='utf-8',errors='replace') as f:
            reader = csv.DictReader(f)
            #Separate the status according to the personality and also create a megaDocument of status
            #print(self.filterWords("This is the book I was requesting"))
            for row in reader:
                #print(self.filterWords(row['STATUS']))
                status = self.filterWords(row['STATUS'])
                if row['cEXT'] == 'y':
                    self.eStatus.append(status)
                if row['cNEU'] == 'y':
                    self.nStatus.append(status)
                if row['cAGR'] == 'y':
                    self.aStatus.append(status)
                if row['cCON'] == 'y' :
                    self.cStatus.append(status)
                if row['cOPN'] == 'y' :
                    self.oStatus.append(status)
                self.megaStatus.append(status)
            
            #Calculate the prior probabilty of each class
        prior = self.calculatePrior(self.eStatus,self.nStatus,self.aStatus,self.cStatus,self.oStatus,self.megaStatus)
        self.priorofE,self.priorofN,self.priorofA,self.priorofC,self.priorofO = prior
        with open("prior.pik","wb") as f:
            dill.dump(prior,f)
        #print("\n Openness: %f\n Conscientiousness: %f\n Extraversion: %f\n Agreeableness: %f\n Neuroticism: %f\n" %(priorofO,priorofC,priorofE,priorofA,priorofN))
        #Calculate likelihood
        #Using Hash Table
        self.hTable = self.generateHash(self.eStatus,self.nStatus,self.aStatus,self.cStatus,self.oStatus,self.megaStatus) 
        #print(pd.DataFrame(self.hTable))
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
   
         
    def generateHash(self,eStatus,nStatus,aStatus,cStatus,oStatus,megaStatus):
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
       megaStatusList = []
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
       for i in megaStatus:
           megaStatusList.extend(i.split())
       #Set each splitted word as an attribute and calculate their frequency
       '''
       print(len(eStatusList))
       print(len(nStatusList))
       print(len(aStatusList))
       print(len(cStatusList))
       print(len(oStatusList))
       print(len(set(megaStatusList)))
       '''

       vocaSize = len(set(megaStatusList))
       with open("vocaSize.pik","wb") as f:
           dill.dump(vocaSize,f)
       self.vSize = vocaSize
       for i in eStatusList[0:1000]:
           eStatusDict[i] = eStatusList.count(i)
       for i in nStatusList[0:1000]:
           nStatusDict[i] = nStatusList.count(i)
       for i in aStatusList[0:1000]:
           aStatusDict[i] = aStatusList.count(i)
       for i in cStatusList[0:1000]:
           cStatusDict[i] = cStatusList.count(i)
       for i in oStatusList[0:1000]:
           oStatusDict[i] = oStatusList.count(i)
       '''
       for i in megaStatusList:
           if i in eStatusList:
               eStatusDict[i] = megaStatus.count(i)
           if i in nStatusList:
               nStatusDict[i] = megaStatus.count(i)
           if i in aStatusList:
               aStatusDict[i] = megaStatus.count(i)
           if i in cStatusList:
               cStatusDict[i] = megaStatus.count(i)
           if i in cStatusList:
               cStatusDict[i] = megaStatus.count(i)
       '''
       #Adjust Valuse: To those attributes present in one class but not in other as if they are left zero doesn't work well
       eStatusDict,nStatusDict,aStatusDict,cStatusDict = self.adjustValue(oStatusDict,eStatusDict,nStatusDict,aStatusDict,cStatusDict) 
       eStatusDict,nStatusDict,aStatusDict,oStatusDict = self.adjustValue(cStatusDict,eStatusDict,nStatusDict,aStatusDict,oStatusDict) 
       eStatusDict,nStatusDict,oStatusDict,cStatusDict = self.adjustValue(aStatusDict,eStatusDict,nStatusDict,oStatusDict,cStatusDict) 
       eStatusDict,oStatusDict,aStatusDict,cStatusDict = self.adjustValue(nStatusDict,eStatusDict,oStatusDict,aStatusDict,cStatusDict)
       oStatusDict,nStatusDict,aStatusDict,cStatusDict = self.adjustValue(eStatusDict,oStatusDict,nStatusDict,aStatusDict,cStatusDict) 
       #Generate a likelihood probability
       for key,value in eStatusDict.items():
           eStatusDict[key] = (value+1)/(len(eStatusList)+vocaSize)
       for key,value in nStatusDict.items():
           nStatusDict[key] = (value+1)/(len(nStatusList)+vocaSize)
       for key,value in aStatusDict.items():
           aStatusDict[key] = (value+1)/(len(aStatusList)+vocaSize)
       for key,value in cStatusDict.items():
           cStatusDict[key] = (value+1)/(len(cStatusList)+vocaSize)
       for key,value in oStatusDict.items():
           oStatusDict[key] = (value+1)/(len(oStatusList)+vocaSize)
       hTable = {'Extraversion':eStatusDict,'Neuroticism':nStatusDict,'Agreebleness':aStatusDict,'Conscientiousness':cStatusDict,'Openness':oStatusDict}
       with open("hashTable.pik","wb") as f:
           dill.dump(hTable,f)  
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

    def calculate(self,personality,word):
       try:
           prob = self.hashTable[personality][word]
       except KeyError:
           prob = 1 / self.vSize
       return prob
    def classify(self,sentence):
        words = sentence.split()
        e = []
        n = []
        a = []
        c = []
        o = []
        for i in words:
            e.append(self.calculate('Extraversion',i))
            n.append(self.calculate('Neuroticism',i))
            a.append(self.calculate('Agreebleness',i))
            c.append(self.calculate('Conscientiousness',i))
            o.append(self.calculate('Openness',i))
        
        priorofE,priorofN,priorofA,priorofC,priorofO = self.priorofE,self.priorofN,self.priorofA,self.priorofC,self.priorofO 
        '''
        print(e)
        print(n)
        print(a)
        print(c)
        print(o)
        '''
        ep = priorofE
        for i in e:
            ep *= i
        np = priorofN
        for i in n:
            np *= i
        ap = priorofA
        for i in a:
            ap *= i
        cp = priorofC
        for i in c:
            cp *= i
        op = priorofO
        for i in o:
            op *= i
        #print("Extraversion: ",math.modf(math.log(ep))[0]* -1, "Neuroticism:",math.modf(math.log(np))[0] * -1 ,"Agreebleness:",math.modf(math.log(ap))[0] * -1 ,"Conscientiousness:",math.modf(math.log(cp))[0] * -1 ,"Openness:",math.modf(math.log(op))[0] * -1 )
        verdict = " "
        extraversion = math.modf(math.log(ep))[0] * -1
        neuroticism = math.modf(math.log(np))[0] * -1
        agreebleness = math.modf(math.log(ap))[0] * -1
        conscientiouness  = math.modf(math.log(cp))[0] * -1
        openness = math.modf(math.log(op))[0] * -1
        if extraversion >= 0.5:
            verdict += "Extraversion "
        if neuroticism >= 0.5:
            verdict += "Neuroticism "
        if agreebleness >= 0.5:
            verdict += "Agreebleness "
        if conscientiouness >= 0.5:
            verdict += "Conscientiousness"
        if openness >= 0.5:
            verdict += "Openness"
        return verdict
    def testImport(self):
        return "sucessful"
    def test(self,file):
        with open(file, 'r',encoding='utf-8',errors='replace') as f:
            reader = csv.DictReader(f)
            totalCount = 0
            countT = 0
            countF = 0
            
            
            for row in reader:
                totalCount += 1
                status = self.filterWords(row['STATUS'])
                verdict = self.classify(status)
                try:
                    for j in verdict.split():
                        if row['cEXT'] == 'y' and j == "Extraversion" :
                            countT += 1
                        if row['cNEU'] == 'y' and j == "Neuroticism" :
                            countT += 1
                            totalCount += 1
                        if row['cAGR'] == 'y' and j == "Agreeableness" :
                            countT += 1
                            totalCount += 1
                        if row['cCON'] == 'y' and j == "Conscientiousness" :
                            countT += 1
                            totalCount += 1
                        if row['cOPN'] == 'y' and j == "Openness" :
                            countT += 1
                            totalCount += 1

                        if row['cEXT'] == 'n' and j not in verdict :
                            countF += 1
                            totalCount += 1
                        if row['cNEU'] == 'n' and j not in verdict :
                            countF += 1
                            totalCount += 1
                        if row['cAGR'] == 'n' and j not in verdict :
                            countF += 1
                            totalCount += 1
                        if row['cCON'] == 'n' and j not in verdict :
                            countF += 1
                            totalCount += 1
                        if row['cOPN'] == 'n' and j not in verdict :
                            countF += 1
                            totalCount += 1
                        
                except AttributeError:
                    continue
           
        accuracy = (countT+countF) / (totalCount)
        print("Accuracy:",accuracy)


if __name__=="__main__":
    try:
        naivebayes = NaiveBayes()
        #naivebayes.train('dataSet/mypersonality_final/mypersonality_final.csv')

        
       #naivebayes.train('trainSet1.csv')
       #naivebayes.test('testSet1.csv')
       #naivebayes.train('trainSet2.csv')
       #naivebayes.test('testSet2.csv')
       #naivebayes.train('trainSet3.csv')
       #naivebayes.test('testSet3.csv')
       #naivebayes.train('trainSet4.csv')
       #naivebayes.test('testSet4.csv')
       #naivebayes.train('trainSet5.csv')
       #naivebayes.test('testSet5.csv')
        toclassify = input("Enter the string to classify:")
        print(naivebayes.classify(toclassify))
        
    except FileNotFoundError:
        print("Training file unavailable")

