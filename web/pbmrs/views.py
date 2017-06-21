from django.shortcuts import render,HttpResponse


# Create your views here.
def home(request):
    return HttpResponse("PBMRS")

def recommend(request):
    return HttpResponse("Recommendation")
