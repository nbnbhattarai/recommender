from django.shortcuts import render,HttpResponse
import sys
sys.path.insert(0,'../../')
from personalityClassifer.naivebayes import NaiveBayes

# Create your views here.
naivebayes = NaiveBayes()
def home(request):
    return render(request, 'pbmrs/index.html')

def personality(request):
    return HttpResponse(naivebayes.testImport())

def recommend(request):
    return HttpResponse("Recommendation")
