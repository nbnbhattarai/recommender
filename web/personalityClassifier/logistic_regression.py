import numpy as np
import pandas as pd
import math
from ast import literal_eval

class LogisticRegression:
	data = None
	X = None
	Y_o = None
	Y_c = None
	Y_e = None
	Y_a = None
	Y_n = None

	theta_o = None
	theta_c = None
	theta_e = None
	theta_a = None
	theta_n = None

	def __init__(self, file = 'wordvector_train.csv'):
		self.load_data(file)
		self.compute_X()
		self.compute_Y_o()
		self.compute_Y_c()
		self.compute_Y_e()
		self.compute_Y_a()
		self.compute_Y_n()
		self.theta_o = np.zeros(len(self.X[0]))
		self.theta_c = np.zeros(len(self.X[0]))
		self.theta_e = np.zeros(len(self.X[0]))
		self.theta_a = np.zeros(len(self.X[0]))
		self.theta_n = np.zeros(len(self.X[0]))

	def load_data(self, file):
		self.data = pd.read_csv(file)
		for i, j in zip(self.data['word_vector'],range(len(self.data['word_vector']))):
			self.data['word_vector'][j] = literal_eval(i)

	def compute_X(self):
		base = np.array([1])
		for i, j in zip(self.data['word_vector'],range(len(self.data['word_vector']))):
			features = np.array(self.data['word_vector'][j])
			features = np.append(base, features)
			if self.X is None:
				self.X = features
			else:
				self.X = np.vstack([self.X, features])

	def compute_Y_o(self):
		self.Y_o = np.array(self.data['class_o'])

	def compute_Y_c(self):
		self.Y_c = np.array(self.data['class_c'])

	def compute_Y_e(self):
		self.Y_e = np.array(self.data['class_e'])

	def compute_Y_a(self):
		self.Y_a = np.array(self.data['class_a'])

	def compute_Y_n(self):
		self.Y_n = np.array(self.data['class_n'])

	def sigmoid(self, z):
		return float(1.0 / float((1.0 + math.exp(-1.0*z))))

	def hypothesis(self, theta, x):
		z = 0
		x= list(x)
		theta = list(theta)
		for i in range(len(theta)):
			z += x[i]*theta[i]
			# print('z: ', z)
			# print('xi: ', x[i])
			# print('theta:',theta[i])
		return self.sigmoid(z)

	def cost_function(self, x, y, theta, m):
		sumOfErrors = 0
		for i in range(m):
			xi = x[i]
			hi = self.hypothesis(theta,xi)
			if y[i] == 1:
				error = y[i] * math.log(hi)
			elif y[i] == 0:
				error = (1-y[i]) * math.log(1-hi)
			sumOfErrors += error
		const = -1/m
		J = const * sumOfErrors
		return J

	def cost_function_derivative(self,x,y,theta,j,m,alpha):
		sumErrors = 0
		for i in range(m):
			xi = x[i]
			xij = xi[j]
			# print('x[i]: ', x[i], 'theta: ', theta)
			hi = self.hypothesis(theta,x[i])
			error = (hi - y[i])*xij
			sumErrors += error
		m = len(y)
		constant = float(alpha)/float(m)
		J = constant * sumErrors
		# print('J:',J)
		return J

	def gradient_descent(self,x,y,theta,m,alpha):
		new_theta = theta
		constant = alpha/m
		# print(new_theta)
		for j in range(len(theta)):
			CFDerivative = self.cost_function_derivative(x,y,theta,j,m,alpha)
			# print(CFDerivative)
			# print(theta[j])
			# print(new_theta[j])
			new_theta[j] = theta[j] - CFDerivative
			# new_theta.append(new_theta_value)
		# print('gd: ',new_theta)
		return new_theta

	def logistic_regression_o(self,alpha,num_iters):
		m = len(self.Y_o)
		for x in range(num_iters):
			# print('before:', self.theta)
			new_theta = self.gradient_descent(self.X,self.Y_o,self.theta_o,m,alpha)
			self.theta_o = new_theta
			# print('after:', self.theta)
			if x % 100 == 0:
				self.cost_function(self.X,self.Y_o,self.theta_o,m)
				# print(self.theta)
				# print(self.cost_function(self.X,self.Y_o,self.theta,m))

	def logistic_regression_c(self,alpha,num_iters):
		m = len(self.Y_c)
		for x in range(num_iters):
			# print('before:', self.theta)
			new_theta = self.gradient_descent(self.X,self.Y_c,self.theta_c,m,alpha)
			self.theta_c = new_theta
			# print('after:', self.theta)
			if x % 100 == 0:
				self.cost_function(self.X,self.Y_c,self.theta_c,m)

	def logistic_regression_e(self,alpha,num_iters):
		m = len(self.Y_e)
		for x in range(num_iters):
			# print('before:', self.theta)
			new_theta = self.gradient_descent(self.X,self.Y_e,self.theta_e,m,alpha)
			self.theta_e = new_theta
			# print('after:', self.theta)
			if x % 100 == 0:
				self.cost_function(self.X,self.Y_e,self.theta_e,m)

	def logistic_regression_a(self,alpha,num_iters):
		m = len(self.Y_a)
		for x in range(num_iters):
			# print('before:', self.theta)
			new_theta = self.gradient_descent(self.X,self.Y_o,self.theta_a,m,alpha)
			self.theta_a = new_theta
			# print('after:', self.theta)
			if x % 100 == 0:
				self.cost_function(self.X,self.Y_o,self.theta_a,m)

	def logistic_regression_n(self,alpha,num_iters):
		m = len(self.Y_n)
		for x in range(num_iters):
			# print('before:', self.theta)
			new_theta = self.gradient_descent(self.X,self.Y_o,self.theta_n,m,alpha)
			self.theta_n = new_theta
			# print('after:', self.theta)
			if x % 100 == 0:
				self.cost_function(self.X,self.Y_o,self.theta_n,m)

lg_train = LogisticRegression()


alpha = 0.2

iterations = 2

# from sklearn.linear_model import LogisticRegression as LG
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
# from sklearn.cross_validation import train_test_split
# x_train, x_test, y_o_train, y_o_test = train_test_split(lg.X, lg.Y_o,test_size = 0.2, random_state = 42, stratify=lg.Y_o)


# iterlist = [1, 5, 10, 20, 50]
# conf_matrix = []
# fscore = []

# for i in range(len(iterlist)):	
# 	lg_o = LG(max_iter = iterlist[i])
# 	lg_o.fit(x_train,y_o_train)
# 	y_o_predict = lg_o.predict(x_test)
# 	conf_matrix.append(confusion_matrix(y_o_test, y_o_predict))
# 	fscore.append(precision_recall_fscore_support(y_o_test, y_o_predict, average = 'micro')[2])
# print(conf_matrix)
# print(fscore)

# lg_c = LG()
# lg_e = LG()
# lg_a = LG()
# lg_n = LG()

# lg_c.fit(lg.X,lg.Y_c)
# lg_e.fit(lg.X,lg.Y_e)
# lg_a.fit(lg.X,lg.Y_a)
# lg_n.fit(lg.X,lg.Y_n)


lg_train.logistic_regression_o(alpha,iterations)
lg_train.logistic_regression_c(alpha,iterations)
lg_train.logistic_regression_e(alpha,iterations)
lg_train.logistic_regression_a(alpha,iterations)
lg_train.logistic_regression_n(alpha,iterations)

lg = LogisticRegression('wordvector_test.csv')

y_o_predict = []
for x in lg.X:
	y_o_predict.append(lg_train.hypothesis(lg.theta_o, x))
accurate = 0
for i in range(len(y_o_predict)):
	if (lg.Y_o[i] == 1 and y_o_predict[i] >= 0.5) or (lg.Y_o[i] == 0 and y_o_predict[i] < 0.5):
		accurate += 1
print('Y_o accuracy:', accurate/len(y_o_predict))

y_c_predict = []
for x in lg.X:
	y_c_predict.append(lg_train.hypothesis(lg.theta_c, x))
accurate = 0
for i in range(len(y_c_predict)):
	if (lg.Y_c[i] == 1 and y_c_predict[i] >= 0.5) or (lg.Y_c[i] == 0 and y_c_predict[i] < 0.5):
		accurate += 1
print('Y_c accuracy:', accurate/len(y_c_predict))

y_e_predict = []
for x in lg.X:
	y_e_predict.append(lg_train.hypothesis(lg.theta_e, x))
accurate = 0
for i in range(len(y_e_predict)):
	if (lg.Y_e[i] == 1 and y_e_predict[i] >= 0.5) or (lg.Y_e[i] == 0 and y_e_predict[i] < 0.5):
		accurate += 1
print('Y_e accuracy:', accurate/len(y_e_predict))

y_a_predict = []
for x in lg.X:
	y_a_predict.append(lg_train.hypothesis(lg.theta_a, x))
accurate = 0
for i in range(len(y_a_predict)):
	if (lg.Y_a[i] == 1 and y_a_predict[i] >= 0.5) or (lg.Y_a[i] == 0 and y_a_predict[i] < 0.5):
		accurate += 1
print('Y_a accuracy:', accurate/len(y_a_predict))

y_n_predict = []
for x in lg.X:
	y_n_predict.append(lg_train.hypothesis(lg.theta_n, x))
accurate = 0
for i in range(len(y_n_predict)):
	if (lg.Y_n[i] == 1 and y_n_predict[i] >= 0.5) or (lg.Y_n[i] == 0 and y_n_predict[i] < 0.5):
		accurate += 1
print('Y_n accuracy:', accurate/len(y_n_predict))


# conf_matrix_o = confusion_matrix(lg.Y_o, y_o_predict)
# conf_matrix_c = confusion_matrix(lg.Y_c, y_c_predict)
# conf_matrix_e = confusion_matrix(lg.Y_e, y_e_predict)
# conf_matrix_a = confusion_matrix(lg.Y_a, y_a_predict)
# conf_matrix_n = confusion_matrix(lg.Y_n, y_n_predict)

# fscore_o = precision_recall_fscore_support(lg.Y_o, y_o_predict, average = 'micro')[2]
# fscore_c = precision_recall_fscore_support(lg.Y_c, y_c_predict, average = 'micro')[2]
# fscore_e = precision_recall_fscore_support(lg.Y_e, y_e_predict, average = 'micro')[2]
# fscore_a = precision_recall_fscore_support(lg.Y_a, y_a_predict, average = 'micro')[2]
# fscore_n = precision_recall_fscore_support(lg.Y_n, y_n_predict, average = 'micro')[2]
# print('cm_y_o:', conf_matrix_o)
# print('cm_y_c:', conf_matrix_c)
# print('cm_y_e:', conf_matrix_e)
# print('cm_y_a:', conf_matrix_a)
# print('cm_y_n:', conf_matrix_n)

# print('fscore_y_o:', fscore_o)
# print('fscore_y_c:', fscore_c)
# print('fscore_y_e:', fscore_e)
# print('fscore_y_a:', fscore_a)
# print('fscore_y_n:', fscore_n)