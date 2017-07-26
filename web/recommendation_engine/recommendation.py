import numpy as np
import copy
import math

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

		#print(utility_matrix_copy)
		#print(system_average)
		#print(user_deviation)
		#print(music_rating_deviation)

		for j in range(len(music_rating_deviation)):
			for i in range(len(user_deviation)):
				#print('i:', i, 'j:', j)
				utility_matrix_copy[j][i] = system_average + user_deviation[i] + music_rating_deviation[j]

		print('baseline:',utility_matrix_copy)
		return utility_matrix_copy

	def collaborative_personality(self, user_similarity_matrix, utility_matrix, k=3):
		for i in range(user_similarity_matrix.shape[0]):
			pass

	def latent_factor(self,utility_matrix,K=2,steps=50000,alpha=0.0002,beta=0.02):
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
                                P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j]- beta * P[i][k])
                                Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
                e = 0
                for i in range(utility_matrix.shape[0]):
                   for j in range(utility_matrix.shape[1]):
                        if R[i][j] > 0:
                            e = e + pow(R[i][j]-np.dot(P[i,:],Q[:,j]),2)
                            for k in range(K):
                                e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
                                if e < 0.001:
                                    break
            return np.dot(P,Q)
if __name__=='__main__':

	recommendation = Recommendation()
	utility_matrix = np.array([[5, 3, 0, 1],[4, 0, 0, 1],[1, 1, 0, 5], [1, 0, 0, 4],[0, 1, 5, 4]])
	print(utility_matrix)
	print(recommendation.latent_factor(utility_matrix))
	recommendation.global_baseline(utility_matrix)
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
