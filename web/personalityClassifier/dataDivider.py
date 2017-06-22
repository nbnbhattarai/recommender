import random
import math
count = 0
step = 0.2
temp = 0
n = int(input("Enter the partition no:"))
with open('dataSet/mypersonality_final/mypersonality_final.csv',errors='replace') as data:
    count = sum(1 for line in data)
    total = step * count
with open('dataSet/mypersonality_final/mypersonality_final.csv',errors='replace') as data:
    with open('testSet'+str(n)+'.csv','w') as test:
        with open('trainSet'+str(n)+'.csv','w') as train:
            header = next(data)
            test.write(header)
            train.write(header)
            for lines in data:
                temp += 1
                if temp >=  math.ceil(total * (n-1)) and temp < math.ceil(total* n):
                    test.write(lines)
                else:
                        train.write(lines)
print(math.ceil(total))
print(count-math.ceil(total))
