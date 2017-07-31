from django.shortcuts import render,HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import views
import dill, sys, simplejson as json, random, string
sys.path.insert(0,'../')
from .database_handler import *
from .utils import get_personality_from_status_data, get_session_id_for_user, get_user_from_sessionid, update_user_data, get_recommendation
from .models import SessionModel, UserModel, MusicModel, UserMusicModel, RecommendationModel

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
        sessionid = request.COOKIES.get('sessionid')
        login_user = None
        recommended_songs = None
        if sessionid != None:
            login_user = get_user_from_sessionid(sessionid=sessionid)
            print('login_user: ', login_user)
            recommended_songs = get_recommendation(login_user)
            print('recommend_song: ', recommended_songs)
        context = {
            'login_user' : login_user,
            'title':'Home',
            'recommended_songs' : recommended_songs,
        }
        if sessionid:
            login_user = get_user_from_sessionid(sessionid=sessionid)
            context['login-user'] = login_user
        return render(request, 'pbmrs/index.html',context)

    def post(self, request, *args, **kwargs):
        user_fbid = request.POST.get('id')
        user_name = request.POST.get('name')
        print('got from post: ', user_name)
        user_posts = request.POST.get('posts')
        user_posts = json.loads(user_posts)
        print('user_posts data : ', user_posts)
        post_combined = ''
        context = {
            'title':'home',
        }
        response = render(request, 'pbmrs/index.html',context)
        # Login user or signup with given facebook data
        if user_fbid != None:
            print('Inside user_fbid')
            user = get_user_by_fbid(user_fbid)
            if user != None:
                print('User already exists!')
                update_user_data(user, user_posts)
            else:
                personality_result = get_personality_from_status_data(user_posts)
                print('personality_result: ', personality_result)
                user = UserModel(fb_id=user_fbid,
                                 name=user_name,
                                 op=personality_result['op'],
                                 cons=personality_result['cons'],
                                 ex=personality_result['ex'],
                                 ag=personality_result['ag'],
                                 neu=personality_result['neu'])
                user.save()
                print('New user added!')
            user = get_user_by_fbid(user_fbid)
            new_sessionid = get_session_id_for_user(user)
            response.set_cookie('sessionid', new_sessionid)
        return response

class LogOutView(views.View):
    def get(self, request, *args, **kwargs):
        sid = request.COOKIES.get('sessionid')
        print('sessionid from logout : ', sid, type(sid))
        response = HttpResponseRedirect(reverse('home'))
        if sid != None:
            print('sessionid is true inside logoutview')
            response.delete_cookie('sessionid')
            sobj = SessionModel.objects.filter(sessionid=sid).first()
            if sobj:
                sobj.delete()
                print('Logout!')
            else:
                print('No Logout!')
        return response

def about_personality(request):
    #return HttpResponse(naivebayes.classify("This is awesome"))
    return render(request,'pbmrs/aboutPersonality.html')

def recommend(request):
    return HttpResponse("Recommendation")
