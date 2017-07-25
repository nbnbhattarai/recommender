import pandas as pd

train = pd.read_csv('trainSet.csv')
newdict = {'status':[],'o':[],'c':[],'e':[],'a':[],'n':[]}
train.sort_values(by="#AUTHID")
authid = ''
for row in train.itertuples():
	if row[1]==authid:
		newdict['status'][-1] += ' ' + row[2]
	else:
		newdict['status'].append(row[2])
		newdict['o'].append((row[12]))
		newdict['c'].append((row[11]))
		newdict['e'].append((row[8]))
		newdict['a'].append((row[10]))
		newdict['n'].append((row[9]))
		authid = row[1]
print(newdict)
df=pd.DataFrame(newdict)
df.to_csv('preprocessed_dataset.csv')
