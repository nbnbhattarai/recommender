import pandas as pd
import csv
import math

class NaiveBayes:
    underweight_count = 0
    overweight_count = 0
    normal_count  = 0
    total_count = 0
    uw_list = []
    ow_list = []
    n_list = []
    total_list = []
    uwHash = {}
    owHash = {}
    nHash={}
    def __init__(self):
        pass
    def train(self,file):
        with open(file,'r') as f:
            self.reader = csv.reader(f)
            list_reader = list(self.reader)
            for row in list_reader[1:]:
                if self.calculateBMI(row) == 'underweight':
                    row.append('underweight')
                    self.uw_list.append(row)
                    self.underweight_count += 1
                if self.calculateBMI(row) == 'overweight':
                    row.append('overweight')
                    self.ow_list.append(row)
                    self.overweight_count += 1
                if self.calculateBMI(row) == 'normal':
                    row.append('normal')
                    self.n_list.append(row)
                    self.normal_count += 1
            self.total_count = self.underweight_count+self.overweight_count+self.normal_count
            self.total_list = self.uw_list + self.ow_list+ self.n_list
            self.uwHash =self.generateHash(self.uw_list)
            self.owHash =self.generateHash(self.ow_list)
            self.nHash =self.generateHash(self.n_list)
            hashtable = self.HashTable(self.nHash,self.owHash,self.uwHash)
            phashtable = pd.DataFrame(hashtable)
            hashtable_prob = pd.DataFrame(self.hashTable_Prob(self.nHash,self.owHash,self.uwHash))
            #print(phashtable)
            print(hashtable_prob)
            print('Normal:',self.normal_count/self.total_count)
            print('Overweight:',self.overweight_count/self.total_count)
            print('Underweight:',self.underweight_count/self.total_count)
    def adjustValue(self,dict1,dict2,dict3):
        for i in dict1:
            if i not in dict2:
                dict2[i] = 0
            if i not in dict3:
                dict3[i] = 0
        for i in dict2:
            if i not in dict1:
                dict1[i] = 0
            if i not in dict3:
                dict3[i] = 0
        for i in dict3:
            if i not in dict1:
                dict1[i] = 0
            if i not in dict2:
                dict2[i] = 0
        return dict1,dict2,dict3
        
    def HashTable(self,dict1,dict2,dict3):
        dict1,dict2,dict3 = self.adjustValue(dict1,dict2,dict3)
        dict ={'Normal':dict1,'Overweight':dict2,'Underweight':dict3}
        return dict
    def hashTable_Prob(self,dict1,dict2,dict3):
        dict1,dict2,dict3 = self.adjustValue(dict1,dict2,dict3)
        for i in dict1:
            dict1[i] = (dict1[i]+1)/(self.normal_count+len(self.n_list))
        for i in dict2:
            dict2[i] = (dict2[i]+1)/(self.overweight_count+len(self.ow_list))
        for i in dict3:
            dict3[i] = (dict3[i]+1)/(self.underweight_count+len(self.uw_list))

        dict ={'Normal':dict1,'Overweight':dict2,'Underweight':dict3}
        return dict
    def generateHash(self,list):
        attributes = {'sex_M':0,'sex_F':0}
        for row in list:
            sex = row[0]
            height = round(float(row[1]))
            weight = int(float(row[2])) - int(float(row[2]))%10
            if row[0] == 'M':
                attributes['sex_M'] += 1
            else:
                attributes['sex_F'] += 1
            if 'ht_'+str(height) in attributes.keys():
                attributes['ht_'+str(height)] += 1
            else:
                attributes['ht_'+str(height)] = 1
            if 'wt_'+str(weight) in attributes.keys():
                attributes['wt_'+str(weight)] += 1
            else:
                attributes['wt_'+str(weight)] = 1
        return attributes 
    def calculateBMI(self,list):
        ht = float(list[1])
        wt = float(list[2])
        ht_feet = int(ht)
        ht_inches = math.ceil((ht - int(ht)) * 10)
        i_factor = 12
        m_factor = 0.025
        actual_ht =((ht_feet * i_factor) + (ht_inches))* m_factor
        bmi = round(wt/(actual_ht**2))
        if bmi<19:
            return 'underweight'
        elif bmi>19 and bmi<25:
            return 'normal'
        else:
            return 'overweight'
    def classify(self,args):
        priorN = self.normal_count/self.total_count
        priorUW = self.underweight_count/self.total_count
        priorOW = self.overweight_count/self.total_count
        sex = args[0]
        height = round((float(args[1])))
        wt = int(float(args[2]))
        weight = wt - (wt%10)
        cheight = 'ht_' + str(height)
        cweight = 'wt_' + str(weight)
        ht = []
        wt = []
        try:
            ht =[self.nHash[cheight],self.uwHash[cheight],self.owHash[cheight]]
            wt =[self.nHash[cweight],self.uwHash[cweight],self.owHash[cweight]]
        except KeyError:
            ht = [0,0,0]
            wt = [0,0,0]
        pN = ((priorN * ht[0]* wt[0])+1)/((self.normal_count**2)+len(self.nHash))
        pUW = ((priorUW * ht[1] * wt[1])+1)/((self.underweight_count**2)+len(self.uwHash))
        pOW = ((priorOW * ht[2] * wt[2])+1)/((self.overweight_count**2)+len(self.owHash))
        if pN>pUW and pN>pOW:
            return 'normal'
        elif pUW > pOW:
          return 'underweight'
        elif pOW > pUW:
            return 'overweight'
        else:
            return 'Cannot be classified'
    def test(self,file):
        count = 0
        with open(file,'r') as f:
            self.reader = csv.reader(f)
            list_reader = list(self.reader)
            for row in list_reader[1:]:
                actual = self.calculateBMI(row)
                calculated = self.classify(row)
                if(actual == calculated):
                    count += 1
            accuracy = (len(list_reader[1:])-count)/len(list_reader[1:])*100
            return accuracy
if __name__=="__main__":
    try:
        naivebayes = NaiveBayes()
        naivebayes.train('trainSet.csv')
        print("Accuracy:",naivebayes.test('testSet.csv'))
        print("Actual BMI for ['M',5,50]:",naivebayes.calculateBMI(['M',5,50]))
        print("Calculated BMI:",naivebayes.classify(['M',5,50]))
    except FileNotFoundError:
        print("File not found")
