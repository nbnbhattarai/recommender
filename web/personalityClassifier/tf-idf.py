''' 
	INPUT : Dataset (CSV)
	OUTPUT : TF, IDF, TF-IDF values in CSV
'''


import csv
import re
import math

from nltk.corpus import stopwords
from collections import defaultdict, OrderedDict

stop_words = stopwords.words('english')	

def tf_calc(dct, doc):
	tfv = OrderedDict()
	word_count = 0.
	
	word_split = re.compile('[^a-zA-Z0-9_\\+\\-/]')
	text = [word.strip().lower() for word in word_split.split(doc)]
	
	for word in text:
		if word not in stop_words and word.isalpha():
			if word not in tfv:
				tfv[word] = 0
			tfv[word] += 1
			dct[word].add(doc)
		word_count += 1.
		
	for word in tfv:
		tfv[word] = tfv[word] / word_count
		#writer.writerow([word, tfv[word]])
		#print(word,"\t",tfv[word],"\n")
	
	return tfv, word_count
	
def main():
	# input dataset path here...
	datapath = "dataSet/mypersonality_final/mypersonality_final.csv"
	
	in_file = open(datapath)
	reader = csv.DictReader(in_file)
	
	pathname = "tf-idf-values.csv"
	out_file = open(pathname,"w")
	writer = csv.writer(out_file, lineterminator='\n')
	writer.writerow(['words','tf','idf','tf-idf'])
	
	docs = []
	dct = defaultdict(set)
	tf = {}
	word_counts = defaultdict(float)

	# tf_calculator
	print("Calculating TF...")
	for row in reader:
		doc = str(row['STATUS'])
		docs.append(doc)
		#print(doc)
		tf[doc], word_counts[doc] = tf_calc(dct,doc)
	#print(len(docs))
	print("Calculating TF... COMPLETE !!!\n")
	
	# idf_calc plus CSV writer
	print("Calculating IDF...")
	for doc in docs:
		for word in tf[doc]:
			idf = math.log(len(docs) / (1+len(dct[word])))
			tfidf = tf[doc][word] * idf
			writer.writerow([word,tf[doc][word],idf, tfidf])
	print("Calculating IDF... COMPLETE !!!\n")
	print("Output filename: ",pathname)
	
if __name__ == "__main__":
	print("Starting TF-IDF.\n")
	main()
	print("\nCOMPLETE !!!")	