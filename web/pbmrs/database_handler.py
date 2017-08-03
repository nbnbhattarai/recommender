from .models import UserModel, UserMusicModel, MusicModel, RecommendationModel
import numpy as np
import operator

def get_user(fb_id):
    try:
        user = Model.objects.get(fb_id=fb_id)
    except:
        return None
    return user

def get_user_by_id(id):
    try:
        user = UserModel.objects.get(pk=id)
    except:
        return None
    return user

def get_user_by_fbid(fbid):
    user = None
    try:
        user = UserModel.objects.get(fb_id=fbid)
    except:
        return None
    return user

def get_music_from_id(music_id):
    try:
        music = MusicModel.objects.get(pk=music_id)
    except:
        return None
    return music

def get_music_rating(Music):
    all_user_music = UserMusicModel.objects.filter(song=Music)
    sum_r = 0.0
    count = 0.0
    for m in all_user_music:
        count += 1
        sum_r += m.rating
    return (sum_r/count)

def get_top_music(n):
    all_music = MusicModel.objects.all()
    music_rating = []
    for m in all_music:
        music_rating.append((m, get_music_rating(m)))
    return sorted(music_rating, key=operator.itemgetter(1), reversed=True)[:n]

def addUser(fb_id, userName, op, cons, ex, ag, neu):
    user = UserModel(fb_id=fb_id, userName=userName, op=op, cons=cons, ex=ex, ag=ag, neu=neu)
    user.save()

def get_utility_matrix():
    utility_matrix = np.zeros((UserModel.objects.count(), MusicModel.objects.count()))
    for usermusic_data in UserMusicModel.objects.all():
        utility_matrix[usermusic_data.user.pk-1][usermusic_data.music.pk-1] = usermusic_data.rating
    return utility_matrix

def get_user_matrix():
	user_matrix = np.zeros((UserModel.objects.count(), 5))
	for user_data in UserModel.objects.all():
		user_matrix[user_data.pk-1] = [user_data.op, user_data.cons, user_data.ex, user_data.ag, user_data.neu]
	return user_matrix


def add_recommendation(utility_matrix):
    all_recommendations = RecommendationModel.objects.all()
    for user_id in range(utility_matrix.shape[0]):
        i_sorted = sorted(enumerate(utility_matrix[user_id]), key=operator.itemgetter(1), reverse=True)
        try:
            print('inside try')
            user_from_db = UserModel.objects.get(pk=(user_id+1))
            print('got user from db')
            recommendation = RecommendationModel.objects.filter(user=user_from_db).first()
            if recommendation is not None:
                recommendation.music.clear()
            else:
                recommendation = RecommendationModel(user=user_from_db)
                print('new recommendation created')
                recommendation.save()
                print('new recommendation saved')
            print('got recommendation from db')
            print('clear recommendation')
            for i,r in i_sorted[:10]:
                if r == 0:
                    break
                print('music adding in recommendation')
                music = get_music_from_id(i+1)
                recommendation.music.add(music)
        except Exception as e:
            print(e)
            print('except in add_recommendation')

def get_recommendation(user):
    try:
        recommendation_model = RecommendationModel.objects.get(user=user)
        musics = [music for music in recommendation_model.music.all()]
    except:
        print('Exception in get_recommendation')
    return musics
