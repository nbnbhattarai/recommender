from personalityClassifier.naivebayes import NaiveBayes
from .database_handler import get_utility_matrix, get_music_from_id
from recommendation_engine.recommendation import Recommendation, get_similar_user_matrix
from .models import SessionModel
import random, string, operator

def get_personality_from_status_data(status_data):
    naivebayes = NaiveBayes()
    status_combined = ''
    for status in status_data.values():
        status_combined += status
    return naivebayes.classify(status_combined)

def get_session_id_for_user(user):
    sid = ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(30))
    session = SessionModel(user=user, sessionid=sid)
    session.save()
    return sid

def get_user_from_sessionid(sessionid):
    try:
        obj = SessionModel.objects.get(sessionid=sessionid)
        return obj.user
    except:
        return None

def update_user_data(user, posts):
    '''
    Update user's data about personality with latest posts result
    '''
    pass

def get_recommendation(user):
    utility_matrix = get_utility_matrix()
    print('utility_matrix: \n')
    lst = [list(tmp) for tmp in utility_matrix]
    for kk in lst:
        print(kk)
    print('utility_matrix row:', utility_matrix.shape[0], ' cols: ', utility_matrix.shape[1])
    _, similar_user_matrix = get_similar_user_matrix(utility_matrix)
    print('similar_user_matrix row:', similar_user_matrix.shape[0], ' cols: ', similar_user_matrix.shape[1])
    recommendation = Recommendation()
    collaborative_success, collaborative_result, combined_result = recommendation.collaborative_personality(similar_user_matrix, utility_matrix)
    print('success?', collaborative_success, collaborative_result, combined_result)
    user_row = combined_result[user.pk-1]
    sorted_songs = sorted(enumerate(user_row), key=operator.itemgetter(1), reverse=True)
    songs = []
    count = 0
    for i,song in sorted_songs:
        if count > 10:
            break
        song = get_music_from_id(i)
        if song != None:
            songs.append(song)
        count += 1
    return songs
