import random
with open('dataSet/mypersonality_final/mypersonality_final.csv',errors='replace') as data:
    with open('testSet5.csv','w') as test:
        with open('trainSet5.csv','w') as train:
            header = next(data)
            test.write(header)
            train.write(header)
            for line in data:
                if random.random() > 0.85:
                    train.write(line)
                else:
                    test.write(line)
