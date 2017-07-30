import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from collections import Counter

def preprocessing():
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
	df=pd.DataFrame(newdict)
	df.to_csv('preprocessed_dataset.csv')


def makefeature():
	data = pd.read_csv('preprocessed_dataset.csv')
	porter = PorterStemmer()
	stopW = (stopwords.words('english')) + ['.', '...', '?', '!', '/', '(', ')', '&', '%', '@', '#', ',', ';', ':', '=', '--', '[', ']']
	goodword = []
	vocab = []
	for row in data['status']:
		token = [porter.stem(i.lower()) for i in word_tokenize(row) if i.lower() not in stopW]
		goodword.append(token)
		vocab += token
	document = list(vocab)
	vocab_count = dict(Counter(vocab))
	sorted_vocab = sorted(vocab_count.items(), key=operator.itemgetter(1))
	vocab = list(dict(sorted_vocab[-200:]))
	# print(vocab)

	wordvector = dict.fromkeys(vocab, [])
	# wordvector.update({'user_status':[],'class_o':[],'class_c':[],'class_e':[],'class_a':[],'class_n':[]})
	newdict = {'word_vector':[]}
	for row in data.itertuples():
		token = [porter.stem(i.lower()) for i in word_tokenize(row[7]) if i.lower() not in stopW]
		vector_dict = dict(Counter(token))
		w = []
		for i in vocab:
			
			if i in vector_dict:
				w.append(vector_dict[i])
			else:
				w.append(0)
		newdict['word_vector'].append(w)
	df=pd.DataFrame(newdict)
	# print(df)
	df.to_csv('wordvector.csv')
	return vocab

