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
            'title':'home',
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
        # Login user or signup with given facebook data
        if user_fbid != None:
            print('Inside user_fbid')
            user = get_user_by_fbid(user_fbid)
            if user != None:
                print('User already exists!')
                update_user_data(user, user_posts)
                recommended_songs = get_recommendation(user)
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
                recommended_songs = get_top_n_recommendation()
                print('New user added!')
            user = get_user_by_fbid(user_fbid)
            new_sessionid = get_session_id_for_user(user)
            context['login_user'] = user
            context['recommended_songs'] = recommended_songs
            response = render(request, 'pbmrs/index.html',context)
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

class ProfileView(views.View):
    def get(self, request, *args, **kwargs):
        sessionid = request.COOKIES.get('sessionid')
        login_user = None
        login_user_op = None
        login_user_ag = None
        login_user_ex = None
        login_user_cons = None
        login_user_neu = None

        if sessionid != None:
            login_user = get_user_from_sessionid(sessionid=sessionid)
            if login_user == None:
                return HttpResponseRedirect(reverse('home'))
            personality_result = {}
            login_user_op = login_user.op * 100
            print('login_user.op',login_user_op)
            login_user_ag = login_user.ag * 100
            print('login_user.ag',login_user_ag)
            login_user_ex = login_user.ex * 100
            print('login_user.ex',login_user_ex)
            login_user_cons = login_user.cons * 100
            print('login_user.cons',login_user_cons)
            login_user_neu = login_user.neu * 100
            print('login_user.neu',login_user_neu)
        else:
            return HttpResponseRedirect(reverse('home'))
        context = {
            'login_user' : login_user,
            'title':'profile',
            'personality_result':personality_result,
            'login_user_op': login_user_op,
            'login_user_ag': login_user_ag,
            'login_user_ex': login_user_ex,
            'login_user_cons': login_user_cons,
            'login_user_neu': login_user_neu,
        }
        return render(request, 'pbmrs/profile.html',context)

class AboutView(views.View):
    def get(self, request, *args, **kwargs):
        sessionid = request.COOKIES.get('sessionid')
        login_user = None
        if sessionid != None:
            login_user = get_user_from_sessionid(sessionid=sessionid)
        context = {
            'login_user' : login_user,
            'title':'about',
        }
        return render(request, 'pbmrs/about.html',context)

def about_personality(request):
    #return HttpResponse(naivebayes.classify("This is awesome"))
    return render(request,'pbmrs/aboutPersonality.html')

def recommend(request):
    return HttpResponse("Recommendation")
