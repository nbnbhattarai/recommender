import numpy as np
import copy
import math
import heapq
import sys
sys.path.append("..")
#from pbmrs import database_handler


user_matrix = np.array([
            [0.1, 0.2, 0.9, 0.2, 0.9],
            [0.3, 0.8, 0.9, 0.2, 0.9],
            [0.1, 0.2, 0.9, 0.2, 0.9],
            [0.1, 0.2, 0.9, 0.2, 0.9],
            [0.1, 0.2, 0.9, 0.2, 0.9],
    ])

def get_similar_user_matrix(user_matrix):
	user_similarity_matrix = np.zeros((user_matrix.shape[0], user_matrix.shape[0]))

	user_matrix_dict = {}
	for i in range(user_matrix.shape[0]):
		for j in range(user_matrix.shape[0]):
			similarity = (np.sum(user_matrix[i]*user_matrix[j]))/(math.sqrt(np.sum(user_matrix[i]**2)) * math.sqrt(np.sum(user_matrix[j]**2)))
			user_matrix_dict.update({(i,j):similarity})
			user_similarity_matrix[i][j] = similarity

	return user_matrix_dict, user_similarity_matrix

def get_k_similar_user_matrix(user_similarity_matrix, user_matrix_dict, k=4):
	user_similarity_matrix_k = np.zeros((user_similarity_matrix.shape[0], k))
	for key, value in user_matrix_dict.items():
		for i in range(k):
			if user_similarity_matrix_k[key[0]][i] < value and key[0] != i:
				user_similarity_matrix_k[key[0]][i] = value

	return user_similarity_matrix_k

class Recommendation():

	def __init__(self):
		pass

	def global_baseline(self, utility_matrix):
		system_average = np.average(utility_matrix)
		user_deviation = system_average - np.mean(utility_matrix, axis=0)
		music_rating_deviation = system_average - np.mean(utility_matrix, axis=1)

		utility_matrix_copy = np.zeros(utility_matrix.shape)
		utility_matrix_2 = copy.deepcopy(utility_matrix)
		#print(utility_matrix_copy)
		#print(system_average)
		#print(user_deviation)
		#print(music_rating_deviation)

		for j in range(len(music_rating_deviation)):
			for i in range(len(user_deviation)):
				#print('i:', i, 'j:', j)
				utility_matrix_copy[j][i] = system_average + user_deviation[i] + music_rating_deviation[j]
				if utility_matrix[j][i] == 0:
					utility_matrix_2[j][i] = utility_matrix_copy[j][i]

		#print('baseline:',utility_matrix_copy, '\nNext baseline: ', utility_matrix_2)
		return utility_matrix_copy, utility_matrix_2

	def get_normalized_matrix(self,utility_matrix):
		original = copy.deepcopy(utility_matrix)
		backup = copy.deepcopy(utility_matrix)
		for i in range(utility_matrix.shape[0]):
			sum = utility_matrix.sum(axis=1)[i]
			row = utility_matrix[i]
			count = len(row[row!=0])
			mean = sum / count
			for j in range(utility_matrix.shape[1]):
				if backup[i][j] != 0:
					backup[i][j] -= mean
		backup2 = copy.deepcopy(backup)
		for i in range(utility_matrix.shape[0]):
			for j in range(utility_matrix.shape[1]):
				if original[i][j] == 0:
					backup[i][j] = -10
		return backup2,backup

	def collaborative_filtering(self, user_similarity_matrix, utility_matrix, k=5):

		#print('usre_matrix:', utility_matrix)
		
		combined_matrix,cf_matrix = copy.deepcopy(utility_matrix),copy.deepcopy(utility_matrix)
		global_baseline_result = self.global_baseline(utility_matrix)[0]
		temp_matrix = utility_matrix - global_baseline_result
		normalized_matrix = self.get_normalized_matrix(utility_matrix)[0]
		similarity_normalized = get_similar_user_matrix(normalized_matrix)[1]

		for i in range(user_similarity_matrix.shape[0]):
			similar = list(user_similarity_matrix[i])
			similar_n = list(similarity_normalized[i])

			#print('similar:',similar)
			music_rating_row = list(utility_matrix[i])
			for j in range(len(music_rating_row)):
				if music_rating_row[j] == 0:
					nearest_neighbor_rating = list(utility_matrix[:,j])
					nearest_neighbor_temp_mat = list(temp_matrix[:,j])
					nearest_neighbor_rating_normalized = list(normalized_matrix[:,j])
					for nl in range(len(nearest_neighbor_rating)):
						if nearest_neighbor_rating[nl] == 0:
							similar[nl] = 0
					nonzero_count = 0
					for sm in similar:
						if sm != 0:
							nonzero_count += 1
					#print('similar: ',j, ' : ' , similar)
					#print('nonzero_count: ', nonzero_count)
					# print(len([ i for i in similar if i != 0]) < k)
					#if (len([ i for i in similar if i != 0]) < k):
					if nonzero_count == 0:
						#print('k :', k)
						#print('fucking Collaborative')
						print('Grey user at',i,"for",j)
						continue
						#return None,None,None
					if nonzero_count < k:
						k = nonzero_count

					similar_k = heapq.nlargest(k, similar)
					#print('fucking similar_k : ', similar_k)
					similar_k_index = []
					for sk in similar_k:
						index = similar.index(sk)
						if index in similar_k_index:
							index = similar.index(sk, index + 1)
						similar_k_index.append(index)
					#print('fucking similar_k_index : ', similar_k)
					product_sim = 0
					sum_sim = 0
					#print('music_rating_row:', music_rating_row)
					#print('nearest_neighbor_rating:', nearest_neighbor_rating)
					#print(similar_k_index)
					for sk in similar_k_index:
						product_sim += ( similar[sk] * nearest_neighbor_rating[sk] )
						sum_sim += similar[sk]
					result = product_sim/sum_sim
					cf_matrix[i,j] = result
					offset = global_baseline_result[i,j]
					product_sim = offset
					sum_sim,result = 0,0
					for sk in similar_k_index:
						product_sim += ( similar[sk] * nearest_neighbor_temp_mat[sk] )
						sum_sim += similar[sk]
					result = product_sim/sum_sim
					combined_matrix[i,j] = result
		return True,cf_matrix, combined_matrix
        

	def latent_factor(self,utility_matrix,K=2,steps=5000,alpha=0.0002,beta=0.02):
		R = copy.deepcopy(utility_matrix)
		N = utility_matrix.shape[0]
		M = utility_matrix.shape[1]
		np.random.seed(0)
		P = np.random.rand(N,K)
		Q = np.random.rand(M,K)
		Q = Q.T
		for step in range(steps):
		    for i in range(utility_matrix.shape[0]):
		        for j in range(utility_matrix.shape[1]):
		            if R[i][j] > 0:
		                eij = R[i][j] - np.dot(P[i,:],Q[:,j])
		                for k in range(K):
		                    eij = eij + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
		                for k in range(K):
		                    P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j]- beta * P[i][k])
		                    Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
		    e = 0
		   #for i in range(utility_matrix.shape[0]):
		   #   for j in range(utility_matrix.shape[1]):
		   #        if R[i][j] > 0:
		   #            e = e + pow(R[i][j]-np.dot(P[i,:],Q[:,j]),2)
		   #            for k in range(K):
		   #                e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
		   #                if e < 0.001:
		   #                    break
		return np.dot(P,Q)

	def model_evaluation(self,predicted, actual):
		count = 0.0
		sum_me = 0.0

		#print('predicted: \n', predicted, ' and \n actual :\n', actual)

		#print('\npredicted val:', predicted[0])
		for i in range(predicted.shape[0]):
			for j in range(predicted.shape[1]):
				if actual[i][j] != 0:
					count += 1
					#print('squared: ', (actual[i, j] - predicted[i, j])**2)
					sum_me += (actual[i,j] - predicted[i,j])**2
		rmse = math.sqrt(sum_me/count)

		#print('rmse:', rmse)
		return rmse

if __name__=='__main__':

    recommendation = Recommendation()
    utility_matrix = np.array([[5.0, 3, 0, 1],[2, 3, 3, 1],[1, 1, 0, 5], [1, 2, 4, 4],[2, 1, 1, 4]])
    percentage = 35.0/100.0
    test_rows, test_cols = math.ceil(percentage * utility_matrix.shape[0]), math.ceil(percentage * utility_matrix.shape[1])
    # test_rows = test_cols = 1
    actual_rating_mat = copy.deepcopy(utility_matrix[:test_rows, :test_cols])
    print('Actual rating mat:\n', actual_rating_mat)
    utility_matrix_2 = copy.deepcopy(utility_matrix)
    utility_matrix[:test_rows, :test_cols] = 0
    
    _, global_result= recommendation.global_baseline(utility_matrix)
    print("Global Baseline:\n",global_result[:test_rows,:test_cols])
    print("RMSE Global Baseline:",recommendation.model_evaluation(global_result[:test_rows,:test_cols],actual_rating_mat))
    
    latent_result= recommendation.latent_factor(utility_matrix,steps=5000,K=5)
    print("Latent factor:\n",latent_result[:test_rows,:test_cols])
    print("RMSE Latent factor:",recommendation.model_evaluation(latent_result[:test_rows,:test_cols],actual_rating_mat))
    
    _,similar_user_rwise = get_similar_user_matrix(utility_matrix_2)
    state, cf, cf_combined = recommendation.collaborative_filtering(similar_user_rwise,utility_matrix,k=2)
    if state:
        print("Collaborative with user rating matrix:\n",cf[:test_rows,:test_cols])
        print("RMSE CF with user rating matrix:",recommendation.model_evaluation(cf[:test_rows,:test_cols],actual_rating_mat))
        print("Collaborative & Global with user rating matrix:\n",cf_combined[:test_rows,:test_cols])
        print("RMSE CF & Global with user rating matrix:",recommendation.model_evaluation(cf_combined[:test_rows,:test_cols],actual_rating_mat))
    
    _,similar_user_pwise = get_similar_user_matrix(user_matrix)
    state, cf_per, cf_combined_per = recommendation.collaborative_filtering(similar_user_pwise,utility_matrix,k=5)
    if state:
        print("Collaborative with personality rating matrix:\n",cf_per[:test_rows,:test_cols])
        print("RMSE CF & Global with personality rating matrix:",recommendation.model_evaluation(cf_per[:test_rows,:test_cols],actual_rating_mat))
        print("Collaborative & Global with personality rating matrix:\n",cf_combined_per[:test_rows,:test_cols])
        print("RMSE CF & Global with personality rating matrix:",recommendation.model_evaluation(cf_combined_per[:test_rows,:test_cols],actual_rating_mat))

    avg_similar = (0.75 * similar_user_rwise + 0.25 * similar_user_pwise)/(0.75+0.25)
    state, cf_avg, cf_combined_avg = recommendation.collaborative_filtering(avg_similar,utility_matrix,k=5)
    if state:
        print("Collaborative with avg rating matrix:\n",cf_per[:test_rows,:test_cols])
        print("RMSE CF with avg rating matrix:",recommendation.model_evaluation(cf_avg[:test_rows,:test_cols],actual_rating_mat))
        print("Collaborative & Global with avg rating matrix:\n",cf_combined_per[:test_rows,:test_cols])
        print("RMSE CF & Global with avg rating matrix:",recommendation.model_evaluation(cf_combined_avg[:test_rows,:test_cols],actual_rating_mat))
    print("Utitlity matrix:\n ",utility_matrix)
    print("Normalized matrix:\n",recommendation.get_normalized_matrix(utility_matrix)[1])
    print("Similar users with rating matrix:\n",similar_user_rwise)
    print("Similar users with personality matrix:\n",similar_user_pwise)
    print("Similar users with avg of both:\n",avg_similar)
    # for step in range(1000,10000,500):
    #     result_latent = recommendation.latent_factor(utility_matrix[:],steps=step)
    #     predicted_latent = result_latent[:test_rows, :test_cols]
    #     print('latent evaluation for step : ', step, ' : ', model_evaluation(predicted_latent, actual_rating_mat))

    #for tk in range(10,30):
    #    result_latent = recommendation.latent_factor(utility_matrix[:],K=tk,steps=1000)
    #    predicted_latent = result_latent[:test_rows, :test_cols]
    #    print('latent evaluation for k : ', tk, ' : ', model_evaluation(predicted_latent, actual_rating_mat))

        # print('latent result: ', result_latent)
    # print('utility_matrix', utility_matrix)
    # _, user_similarity_matrix_personality = get_similar_user_matrix(user_matrix)
    # _, user_similarity_matrix_rating = get_similar_user_matrix(utility_matrix)
    # print('rating similarity:',user_similarity_matrix_rating)
    # print('\n =======================\nutility_matrix_2:', utility_matrix_2)
    #
    # collaborative_success, collaborative_result, collaborative_result_combined = recommendation.collaborative_personality(user_similarity_matrix_rating, utility_matrix)
    #
    # print('result collaborative combined:\n', collaborative_result)
    #
	# if not collaborative_success:
	# 	print('Using global baseline....')
	# 	_,collaborative_result = recommendation.global_baseline(utility_matrix_2)
	# print('Collaborative filtering: ', collaborative_result)
    #
	# predicted_baseline = np.array(recommendation.global_baseline(utility_matrix_2))[0][:test_rows, :test_cols]
	# predicted_latent = result_latent[:test_rows, :test_cols]
	# if collaborative_success:
    
    # for step in range(1000,10000,500):
    #     result_latent = recommendation.latent_factor(utility_matrix[:],steps=step)
    #     predicted_latent = result_latent[:test_rows, :test_cols]
    #     print('latent evaluation for step : ', step, ' : ', model_evaluation(predicted_latent, actual_rating_mat))

    #for tk in range(10,30):
    #    result_latent = recommendation.latent_factor(utility_matrix[:],K=tk,steps=1000)
    #    predicted_latent = result_latent[:test_rows, :test_cols]
    #    print('latent evaluation for k : ', tk, ' : ', model_evaluation(predicted_latent, actual_rating_mat))

        # print('latent result: ', result_latent)
    # print('utility_matrix', utility_matrix)
    # _, user_similarity_matrix_personality = get_similar_user_matrix(user_matrix)
    # _, user_similarity_matrix_rating = get_similar_user_matrix(utility_matrix)
    # print('rating similarity:',user_similarity_matrix_rating)
    # print('\n =======================\nutility_matrix_2:', utility_matrix_2)
    #
    # collaborative_success, collaborative_result, collaborative_result_combined = recommendation.collaborative_personality(user_similarity_matrix_rating, utility_matrix)
    #
    # print('result collaborative combined:\n', collaborative_result)
    #
	# if not collaborative_success:
	# 	print('Using global baseline....')
	# 	_,collaborative_result = recommendation.global_baseline(utility_matrix_2)
	# print('Collaborative filtering: ', collaborative_result)
    #
	# predicted_baseline = np.array(recommendation.global_baseline(utility_matrix_2))[0][:test_rows, :test_cols]
	# predicted_latent = result_latent[:test_rows, :test_cols]
	# if collaborative_success:
	# 	predicted_collaborative = collaborative_result[:test_rows, :test_cols]
	# 	predicted_collaborateive_combined = collaborative_result_combined[:test_rows, :test_cols]
	# 	print('collaborative evaluation: ', model_evaluation(predicted_collaborative, actual_rating_mat))
	# 	print('combined evaluation: ', model_evaluation(predicted_collaborateive_combined, actual_rating_mat))
    #
	# print('baseline evaluation: ', model_evaluation(predicted_baseline, actual_rating_mat))
	# print('latent evaluation: ', model_evaluation(predicted_latent, actual_rating_mat))

	#similar_user, su_mat = get_similar_user_matrix(user_matrix)
	#print('+++++++++++++++++')
	#print(similar_user)

	#print('+++++++++++++++++')
	#print(su_mat)

	# similar_user_sorted = sorted(similar_user, reverse=True)
	# k = 3
	# k_matrix = np.zeros((su_mat.shape[0], k))
	# for (a,b) in similar_user_sorted:
	# 	print(a,b)
	# 	if k_matrix[a][k]
	# 		k_matrix[a]

	# for k,v in similar_user.items():
	# 	if k[0] == 1:
	# 		l.append([k,v])
	# 		print(l)

	#print(get_k_similar_user_matrix(su_mat, similar_user, k=4))
