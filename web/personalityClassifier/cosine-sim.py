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
	
	return tfv, word_count

def get_doc_vec(doc,docs):
	dct = defaultdict(set)
	tf = {}
	word_counts = defaultdict(float)
	tf[doc], word_counts[doc] = tf_calc(dct,doc)
#	for word in tf[doc]:
#		print(word,"\t\t\t\t\t",tf[doc][word])
	doc_vec = [tf[doc][word] for word in tf[doc]]
	#print("\nTF Vector for '",doc,"' is ",tf,"\n")
	
	tfidf = {}
	for word in tf[doc]:
		idf = math.log((len(docs)+1) / (1+len(dct[word])))
		tfidf[word] = tf[doc][word] * idf
	#print("TFIDF for '",doc,"' is ",tfidf)
	return tfidf
	
def get_cosine(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])
	
	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)
	
	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

def main():
	datapath = "dataSet/mypersonality_final/mypersonality_final.csv"
	
	in_file = open(datapath)
	reader = csv.DictReader(in_file)
	docs = []
	for row in reader:
		doc = str(row['STATUS'])
		#print(doc)
		docs.append(doc)
	'''
	text1 = 'likes how the day sounds in this new song'
	text2 = 'complete different sentence likes'
	
	docs.append(text1)
	docs.append(text2)
	
	tfidf1 = get_doc_vec(text1,docs)
	tfidf2 = get_doc_vec(text2,docs)
	
	cosine = get_cosine(tfidf1,tfidf2)
	print('\nCosine similarity:', cosine)
	'''
	query = input("Enter the string to classify:")
	docs.append(query)
	
	cosine={}
	for doc in docs:
		tf1 = get_doc_vec(doc,docs)
		tf2 = get_doc_vec(query,docs)
		cosine[doc] = get_cosine(tf1,tf2)
		'''	
		if cosine[doc] > 0.0:
			print("cos_sim = ",cosine[doc])
		'''	
		print("cos_sim = ",cosine[doc])
		# python unicode issue here
		#print('\n cosine similarity between\n',doc.encode('utf-8'),'\n and \n',query.encode('utf-8'),'\n is cos_sim_value = ',cosine) 
	
if __name__ == "__main__":
	print("Starting cosine similarity.\n")
	main()
	print("\nCOMPLETE !!!")	