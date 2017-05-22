import numpy as np
from scipy import optimize
import os

class NeuralNetwork(object):
	def __init__(self, wf = 'w.txt', structure = [1, 2, 2, 7, 1]):
		self.layers = structure
		self.construct()
		self.wf = wf
		self.loadWeights()

	def construct(self):
		self.Weights = []
		for n in range(len(self.layers)-1):
			self.Weights.append(np.random.randn(self.layers[n], self.layers[n+1]))

	def forward(self, X):
		self.z = []
		self.a = []
		self.a.append(X)
		for n in range(len(self.Weights)):
			self.z.append(np.dot(self.a[n], self.Weights[n]))
			self.a.append(self.sigmoid(self.z[n]))
		return self.a[len(self.a)-1]

	def sigmoid(self, z):
		return 1/(1+np.exp(-z))

	def sigmoidPrime(self, z):
		return np.exp(-z)/((1+np.exp(-z))**2)

	def getParams(self):
		params = []
		for n in range(len(self.Weights)):
			params = np.append(params, self.Weights[n].ravel())
		return params

	def setParams(self, params):
		start = end = 0
		for n in range(len(self.Weights)):
			end = start + self.layers[n]*self.layers[n+1]
			self.Weights[n] = np.reshape(params[start:end], (self.layers[n], self.layers[n+1]))
			start = end

	def costFunction(self, X, y):
		self.yHat = self.forward(X)
		J = 0.5*sum(sum((y-self.yHat)**2))
		return J

	def costFunctionPrime(self, X, y):
		self.yHat = self.forward(X)
		self.dJdW = []
		delta = np.multiply(-(y-self.yHat), self.sigmoidPrime(self.z[len(self.z)-1]))
		for n in range(len(self.Weights)):
			self.dJdW.append(np.dot(self.a[len(self.a)-(n+2)].T, delta))
			if n == len(self.Weights)-1: break
			delta = np.dot(delta, self.Weights[len(self.Weights)-(n+1)].T)*self.sigmoidPrime(self.z[len(self.z)-(n+2)])
		self.dJdW.reverse()
		return self.dJdW

	def computeGradients(self, X, y):
		dJdW = self.costFunctionPrime(X, y)
		params = []
		for n in range(len(dJdW)):
			params = np.append(params, self.dJdW[n].ravel())
		return params

	def loadWeights(self):
		if self.weightFileExist():
			self.setParams(np.loadtxt(self.wf))

	def saveWeights(self):
		np.savetxt(self.wf, self.getParams())

	def weightFileExist(self):
		return os.path.isfile(self.wf)

	def deleteWeightsFile(self):
		if self.weightFileExist():
			os.remove(self.wf)

class Trainer(object):
	def __init__(self, N):
		self.N = N

	def save(self):
		self.N.saveWeights()

	def load(self):
		self.N.loadWeights()

	def costFunctionWrapper(self, params, X, y):
		self.N.setParams(params)
		cost = self.N.costFunction(X, y)
		grad = self.N.computeGradients(X, y)
		return cost, grad

	def callbackF(self, params):
		self.N.setParams(params)
		self.J.append(self.N.costFunction(self.X, self.y))

	def train(self, X, y):
		self.X = X
		self.y = y
		self.J = []
		self.load()

		params0 = self.N.getParams()
		options = {'maxiter':1000000, 'maxfev':1000000}

		_res = optimize.minimize(self.costFunctionWrapper, params0,
			jac = True, method='L-BFGS-B', args=(X,y), options=options,
			callback=self.callbackF)

		self.N.setParams(_res.x)
		self.optimizationResults = _res
		self.save()
