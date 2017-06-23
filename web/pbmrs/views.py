from django.shortcuts import render,HttpResponse
import dill 
import sys
sys.path.insert(0,'../')
from personalityClassifier.naivebayes import NaiveBayes
# Create your views here.
naivebayes = NaiveBayes()
#naivebayes.classify("hello")
def home(request):
    #print(request.method)
    posts = ""
    if request.method == 'POST':
        print("start here")
        print(request.POST['posts'])
        posts = request.POST['posts']
    personality = naivebayes.classify(posts)
    test = {'test':posts,'classifier':personality}
    return render(request, 'pbmrs/index.html',test)

def about_personality(request):
    #return HttpResponse(naivebayes.classify("This is awesome"))
    return render(request,'pbmrs/aboutPersonality.html')

def recommend(request):
    return HttpResponse("Recommendation")
