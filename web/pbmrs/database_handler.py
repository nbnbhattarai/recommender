from .models import User, UserMusic, Music, Recommendation
import numpy as np

def get_user(fb_id):
    try:
        user = User.objects.get(fb_id=fb_id)
    except:
        return None
    return user

def get_music_from_id(music_id):
    try:
        music = Music.objects.get(pk=music_id)
    except:
        return None
    return music

def get_music_rating(Music):
    all_user_music = UserMusic.objects.filter(song=Music)
    sum_r = 0.0
    count = 0.0
    for m in all_user_music:
        count += 1
        sum_r += m.rating
    return (sum_r/count)

def get_top_music(n):
    all_music = Music.objects.all()
    music_rating = []
    for m in all_music:
        music_rating.append((m, get_music_rating(m)))
    return sorted(music_rating, key=operator.itemgetter(1), reversed=True)[:n]

def addUser(fb_id, userName, op, cons, ex, ag, neu):
    user = User(fb_id=fb_id, userName=userName, op=op, cons=cons, ex=ex, ag=ag, neu=neu)
    user.save()

def get_utility_matrix(UserMusic):
    utility_matrix = np.zeros((User.objects.count(), Music.objects.count()))
    usermusic_data = UserMusic.objects.all():
        utility_matrix[usermusic_data.user.pk][usermusic_data.music.pk] = usermusic_data.rating
    return usermusic_data
