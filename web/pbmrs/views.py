from django.shortcuts import render,HttpResponse
import dill
import sys
from django import views
sys.path.insert(0,'../')
from personalityClassifier.naivebayes import NaiveBayes
# Create your views here.
naivebayes = NaiveBayes()

#naivebayes.classify("hello")

class classifyPersonality(views.View):
    def get(self, request):
        print("Get request")
        print(request.GET.get('posts'))
        posts = request.GET.get('posts')
        if not posts:
            return HttpResponse('<h1>No Posts</h1>')
        personality = naivebayes.classify(posts)
        context = {'classifier':personality}
        return render(request, 'pbmrs/classifiedPersonality.html',context)

class Home(views.View):
    def get(self, request, *args, **kwargs):
        posts = ""
        print("get request")
        print(request.GET.get('posts'))
        posts = request.GET.get('posts')
        print('posts: ', posts)
        #if not posts:
        #    return HttpResponse('<h1>No posts</h1>')
        personality = 'No posts'
        if posts:
            personality = naivebayes.classify(posts)
        context = {'posts':posts,'classifier':personality}
        return render(request, 'pbmrs/index.html',context)

    def post(self, request, *args, **kwargs):
        print('request.POST')
        context = {
        }
        return render(request, 'pbmrs/index.html',context)

def about_personality(request):
    #return HttpResponse(naivebayes.classify("This is awesome"))
    return render(request,'pbmrs/aboutPersonality.html')

def recommend(request):
    return HttpResponse("Recommendation")
