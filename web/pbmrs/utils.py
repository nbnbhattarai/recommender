from personalityClassifier.naivebayes import NaiveBayes
from .database_handler import get_utility_matrix, get_music_from_id, get_user_matrix
from recommendation_engine.recommendation import Recommendation, get_similar_user_matrix
from .models import SessionModel
import random, string, operator, math, copy

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

def get_recommendation_old(user):
    utility_matrix = get_utility_matrix()
    user_matrix = get_user_matrix()

    test_percentage = 0.2
    test_rows, test_cols = math.ceil(test_percentage * utility_matrix.shape[0]), math.ceil(test_percentage * utility_matrix.shape[1])

    _, similar_user_matrix = get_similar_user_matrix(user_matrix)

    actual_rating_mat = copy.deepcopy(utility_matrix[:test_rows, :test_cols])
    utility_matrix_backup = copy.deepcopy(utility_matrix)
    utility_matrix[:test_rows, :test_cols] = 0
    _, similar_rating_matrix = get_similar_user_matrix(utility_matrix)


    #print('similar_user_matrix row:', similar_user_matrix.shape[0], ' cols: ', similar_user_matrix.shape[1])
    recommendation = Recommendation()
    baseline_result,_ = recommendation.global_baseline(utility_matrix)
    # train_rating_matrix_baseline = copy.deepcopy(baseline_result[:test_rows, :test_cols])
    # print('baseline_model evaluation: ', model_evaluation(train_rating_matrix_baseline, actual_rating_mat))

    # collaborative_success, collaborative_result, combined_result = recommendation.collaborative_filtering(similar_rating_matrix, utility_matrix)
    # train_rating_matrix_cf = copy.deepcopy(collaborative_result[:test_rows, :test_cols])
    # print('cf model evaluation: ', model_evaluation(train_rating_matrix_cf, actual_rating_mat))

    # train_rating_matrix_cf_combined = copy.deepcopy(combined_result[:test_rows, :test_cols])
    # print('cf_combined model evaluation: ', model_evaluation(train_rating_matrix_cf_combined, actual_rating_mat))

    # collaborative_success_u, collaborative_result_u, combined_result_u = recommendation.collaborative_filtering(similar_user_matrix, utility_matrix)
    # train_rating_matrix_cf_u = copy.deepcopy(collaborative_result_u[:test_rows, :test_cols])
    # print('cf model evaluation: ', model_evaluation(train_rating_matrix_cf_u, actual_rating_mat))

    # train_rating_matrix_cf_combined_u = copy.deepcopy(combined_result_u[:test_rows, :test_cols])
    # print('cf_combined model evaluation: ', model_evaluation(train_rating_matrix_cf_combined_u, actual_rating_mat))

    # latent_result = recommendation.latent_factor(utility_matrix)
    # train_rating_matrix_latent = copy.deepcopy(latent_result[:test_rows, :test_cols])
    # print('latent_model evaluation: ', model_evaluation(train_rating_matrix_latent, actual_rating_mat))



    # if collaborative_success == None:
    #     combined_result,_ = recommendation.global_baseline(utility_matrix)
    # print('success?', collaborative_success, collaborative_result, combined_result)
    user_row = baseline_result[user.pk-1]
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
