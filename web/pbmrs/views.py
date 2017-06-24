from django.shortcuts import render,HttpResponse
import dill 
import sys
sys.path.insert(0,'../')
from personalityClassifier.naivebayes import NaiveBayes
# Create your views here.
naivebayes = NaiveBayes()
#naivebayes.classify("hello")
def classifyPersonality(request):
    posts = ""
    if request.method == 'GET':
        print("get request")
        print(request.GET.get('posts'))
    personality = naivebayes.classify(posts)
    test = {'test':posts,'classifier':personality}
    return render(request, 'pbmrs/classifiedPersonality.html',test)

def home(request):
    #print(request.method)
    posts = ""
    if request.method == 'POST':
        print("start here")
        print(request.POST)
        posts = request.POST['posts']
    if request.method == 'GET':
        print("get request")
        print(request.GET.get('posts'))
    personality = naivebayes.classify(posts)
    test = {'test':posts,'classifier':personality}
    return render(request, 'pbmrs/index.html',test)

def about_personality(request):
    #return HttpResponse(naivebayes.classify("This is awesome"))
    return render(request,'pbmrs/aboutPersonality.html')

def recommend(request):
    return HttpResponse("Recommendation")
