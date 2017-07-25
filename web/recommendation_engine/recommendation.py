import numpy as np

class Recommendation():
	
	def __init__(self):
		pass

	def global_baseline(self, utility_matrix):
		system_average = np.average(utility_matrix)
		user_deviation = system_average - np.mean(utility_matrix, axis=0) 
		music_rating_deviation = system_average - np.mean(utility_matrix, axis=1)

		utility_matrix_copy = np.zeros(utility_matrix.shape)

		print(utility_matrix_copy)
		print(system_average)
		print(user_deviation)
		print(music_rating_deviation)

		for j in range(len(music_rating_deviation)):
			for i in range(len(user_deviation)):
				print('i:', i, 'j:', j)
				utility_matrix_copy[j][i] = system_average + user_deviation[i] + music_rating_deviation[j]

		print('umatrix:',utility_matrix_copy)
		return utility_matrix_copy


	def collaborative_personality(self):
		pass

	def latent_factor(self):
		pass

if __name__=='__main__':

	recommendation = Recommendation()
	utility_matrix = np.array([
			[1,2],
			[5,3],
			[4,0],
		])
	recommendation.global_baseline(utility_matrix)