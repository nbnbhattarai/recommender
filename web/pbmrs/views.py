from django.shortcuts import render,HttpResponse
import dill 
import sys
sys.path.insert(0,'../')
from personalityClassifier.naivebayes import NaiveBayes
# Create your views here.
naivebayes = NaiveBayes()
#naivebayes.classify("hello")
def home(request):
    return render(request, 'pbmrs/index.html')

def personality(request):
    return HttpResponse(naivebayes.classify("This is awesome"))

def recommend(request):
    return HttpResponse("Recommendation")
