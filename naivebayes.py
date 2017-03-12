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

if __name__=="__main__":
    try:
        naivebayes = NaiveBayes()
        naivebayes.train('dataSet/mypersonality_final/mypersonality_final.csv')
    except FileNotFoundError:
        print("Training file unavailable")

